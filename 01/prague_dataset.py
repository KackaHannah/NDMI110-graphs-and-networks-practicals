import csv
import os
import sys
import urllib.request
import zipfile
from collections import defaultdict

import networkx as nx


class PIDNetwork:
    """Prague PID GTFS network loader for metro+tram stop graph.

    The loader caches GTFS text files locally, builds a directed multigraph of
    stop-to-stop segments, and stores average travel time on each edge.
    """

    def __init__(
        self,
        cache_dir="cache/",
        zip_url="https://data.pid.cz/PID_GTFS.zip",
    ):
        self.cache_dir = cache_dir
        self.zip_url = zip_url
        self.required_files = ["stops.txt", "stop_times.txt", "trips.txt", "routes.txt"]

        self._ensure_cached_files()

        self.stops = self._read_csv("stops.txt")
        self.stop_times = self._read_csv("stop_times.txt")
        self.trips = self._read_csv("trips.txt")
        self.routes = self._read_csv("routes.txt")

        self.graph = self._build_graph()

    def _ensure_cached_files(self):
        os.makedirs(self.cache_dir, exist_ok=True)
        missing_files = [
            name
            for name in self.required_files
            if not os.path.exists(os.path.join(self.cache_dir, name))
        ]

        if not missing_files:
            print("[OK] Using cached PID GTFS files", file=sys.stderr)
            return

        print("[INFO] Downloading PID GTFS dataset...", file=sys.stderr)
        zip_path = os.path.join(self.cache_dir, "PID_GTFS.zip")
        tmp_path = f"{zip_path}.tmp"

        urllib.request.urlretrieve(self.zip_url, filename=tmp_path)
        os.replace(tmp_path, zip_path)

        print("[INFO] Extracting required GTFS files...", file=sys.stderr)
        with zipfile.ZipFile(zip_path) as zf:
            available = set(zf.namelist())
            for name in self.required_files:
                if name not in available:
                    raise FileNotFoundError(f"Missing required file in ZIP: {name}")
                zf.extract(name, path=self.cache_dir)

        print("[OK] Dataset cached", file=sys.stderr)

    def _read_csv(self, filename):
        file_path = os.path.join(self.cache_dir, filename)
        with open(file_path, newline="", encoding="utf-8") as handle:
            return [row for row in csv.DictReader(handle)]

    def _build_graph(self):
        selected_route_ids = {
            row["route_id"]
            for row in self.routes
            if row.get("route_type") in {"0", "1"}
        }

        selected_trips = {}
        for row in self.trips:
            route_id = row.get("route_id")
            direction_id = row.get("direction_id", "")
            if route_id not in selected_route_ids:
                continue
            key = (route_id, direction_id)
            if key not in selected_trips:
                selected_trips[key] = row["trip_id"]

        selected_trip_ids = set(selected_trips.values())

        valid_zone_ids = {"0", "P", "B", "0,B", "P,0"}
        stop_rows = [
            row
            for row in self.stops
            if row.get("zone_id") in valid_zone_ids and row.get("stop_name")
        ]

        stop_name_by_id = {
            row["stop_id"]: row["stop_name"]
            for row in stop_rows
            if row.get("stop_id") and row.get("stop_name")
        }

        stop_info_by_name = {}
        for row in stop_rows:
            stop_name = row["stop_name"]
            if stop_name in stop_info_by_name:
                continue
            lon_text = row.get("stop_lon") or ""
            lat_text = row.get("stop_lat") or ""
            if lon_text == "" or lat_text == "":
                continue
            try:
                lon_value = float(lon_text)
                lat_value = float(lat_text)
            except ValueError:
                continue
            stop_info_by_name[stop_name] = {"x": lon_value, "y": lat_value}

        selected_stop_times = [
            row
            for row in self.stop_times
            if row.get("trip_id") in selected_trip_ids
            and row.get("stop_id") in stop_name_by_id
        ]

        sorted_stop_times = sorted(
            selected_stop_times,
            key=lambda row: (row["trip_id"], int(row["stop_sequence"])),
        )

        times_by_trip = defaultdict(list)
        for row in sorted_stop_times:
            times_by_trip[row["trip_id"]].append(
                {
                    "stop_name": stop_name_by_id[row["stop_id"]],
                    "arrival": row.get("arrival_time", ""),
                    "departure": row.get("departure_time", ""),
                }
            )

        segment_times = defaultdict(list)
        for rows in times_by_trip.values():
            for current_row, next_row in zip(rows, rows[1:]):
                from_stop = current_row["stop_name"]
                to_stop = next_row["stop_name"]
                dep_seconds = self._parse_gtfs_time(current_row["departure"])
                arr_seconds = self._parse_gtfs_time(next_row["arrival"])
                if dep_seconds is None or arr_seconds is None:
                    continue
                travel_time_min = (arr_seconds - dep_seconds) / 60.0
                if travel_time_min < 0:
                    continue
                segment_times[(from_stop, to_stop)].append(travel_time_min)

        avg_segment_time = {
            pair: (sum(values) / len(values))
            for pair, values in segment_times.items()
            if values
        }

        graph = nx.MultiDiGraph()
        for rows in times_by_trip.values():
            stop_names = [row["stop_name"] for row in rows]
            for from_stop, to_stop in zip(stop_names, stop_names[1:]):
                avg_time_min = avg_segment_time.get((from_stop, to_stop))
                if avg_time_min is None:
                    continue
                graph.add_edge(
                    from_stop,
                    to_stop,
                    avg_time_min=float(avg_time_min),
                )

        nx.set_node_attributes(graph, stop_info_by_name)
        return graph

    @staticmethod
    def _parse_gtfs_time(time_text):
        if not time_text:
            return None
        parts = time_text.split(":")
        if len(parts) != 3:
            return None
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return hours * 3600 + minutes * 60 + seconds
