import os

filename = "day11.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

machine_dict = {}  # resolve label to Machine instance
non_resolved_machines = set()


class Machine:
    def __init__(self, label, connected_labels):
        self._label = label
        self.connected_labels = connected_labels
        self.paths_out = 0
        self.paths_viafft = 0
        self.paths_viadac = 0
        self.paths_viaboth = 0
        self.fully_resolved_paths = False

    @property
    def label(self):
        return self._label

    def get_connected(self):
        self.connected = set()
        for cl in self.connected_labels:
            if cl == "out":
                self.paths_out += 1
                continue
            self.connected.add(machine_dict[cl])

        if len(self.connected) == 0:
            self.fully_resolved_paths = True
            return True
        return False

    def resolve_paths(self):
        for conn in self.connected.copy():
            if conn.fully_resolved_paths:
                self.connected.remove(conn)
                self.paths_out += conn.paths_out

                self.paths_viafft += conn.paths_viafft
                self.paths_viadac += conn.paths_viadac
                self.paths_viaboth += conn.paths_viaboth

                if conn.label == "dac":
                    self.paths_viadac += conn.paths_out
                    self.paths_viaboth += conn.paths_viafft

                if conn.label == "fft":
                    self.paths_viafft += conn.paths_out
                    self.paths_viaboth += conn.paths_viadac

        if len(self.connected) == 0:
            self.fully_resolved_paths = True
            return True
        return False

    def __hash__(self):
        return hash(self._label)

    def __eq__(self, other):
        if not isinstance(other, Machine):
            return False
        return self._label == other._label

    def __repr__(self):  # makes debugging a lot easier :))
        return f"Machine({self._label})"


for line in txt.split("\n"):
    label, connected = line.split(": ")
    connected = connected.split()
    machine_instance = Machine(label, connected)
    machine_dict[label] = machine_instance
    non_resolved_machines.add(machine_instance)

for machine in machine_dict.values():
    if machine.get_connected():
        non_resolved_machines.remove(machine)

while len(non_resolved_machines) > 0:
    for m in non_resolved_machines.copy():
        if m.resolve_paths():
            non_resolved_machines.remove(m)

part1 = machine_dict["you"].paths_out
part2 = machine_dict["svr"].paths_viaboth

print("Part 1:", part1)
print("Part 2:", part2)
