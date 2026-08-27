from typing import Any

def surface_data_initialization_x(circuit_builder, distance, offset):
    for height in range(distance):
        for width in range(distance):
            circuit_builder.rx((1 + width + offset[0], 1 + height + offset[1]))

def surface_ancilla_initialization_x(circuit_builder, distance, offset):
    for height in range(distance - 1):
        for width in range(distance - 1):
            if (height + width) % 2 == 0:
                circuit_builder.rz((1.5 + width + offset[0], 1.5 + height + offset[1]))
            else:
                circuit_builder.rx((1.5 + width + offset[0], 1.5 + height + offset[1]))
    for width in range(2):
        for height in range(distance // 2):
            circuit_builder.rz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]))
    height = 1
    for width in range(distance // 2):
        circuit_builder.rx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]))

def surface_ancilla_initialization_x_boundary(circuit_builder, distance, offset):
    height = 0
    for width in range(distance // 2):
        circuit_builder.rx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]))

def surface_cnot(circuit_builder, distance , offset, rotation, tick):
    surface_rotate_x = rotation[0]
    surface_rotate_z = rotation[1]
    for height in range(distance - 1):
        for width in range(distance - 1):
            if height == 0 and width == distance - 4:
                continue
            if (height + width) % 2 == 0:
                circuit_builder.cnot((1.5 + surface_rotate_z[tick][0] + width + offset[0], 1.5 + surface_rotate_z[tick][1] + height + offset[1]), (1.5 + width + offset[0], 1.5 + height + offset[1]))
            else:
                circuit_builder.cnot((1.5 + width + offset[0], 1.5 + height + offset[1]), (1.5 + surface_rotate_x[tick][0] + width + offset[0], 1.5 + surface_rotate_x[tick][1] + height + offset[1]))

    if tick == 0 or tick == 1:
        width = 0
        for height in range(distance // 2):
            # circuit_builder.rz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]))
            circuit_builder.ideal([(0.5 + width * distance + offset[0], 1.5 + height * 2 + width + offset[1])])
        width = 1
        for height in range(distance // 2):
            circuit_builder.cnot((0.5 + distance * width + surface_rotate_z[tick][0] + offset[0], 2.5 + surface_rotate_z[tick][1] + height * 2 - width + offset[1]), (0.5 + distance * width + offset[0], 2.5 + height * 2 - width + offset[1]))
        height = 1
        for width in range(distance // 2):
            circuit_builder.cnot((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), (1.5 + surface_rotate_x[tick][0] + width * 2 + height + offset[0], 0.5 + height * distance + surface_rotate_x[tick][1] + offset[1]))

    if tick == 2 or tick == 3:
        width = 1
        for height in range(distance // 2):
            # circuit_builder.rz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]))
            circuit_builder.ideal([(0.5 + width * distance + offset[0], 1.5 + height * 2 + width + offset[1])])
        width = 0
        for height in range(distance // 2):
            circuit_builder.cnot((0.5 + distance * width + surface_rotate_z[tick][0] + offset[0], 2.5 + surface_rotate_z[tick][1] + height * 2 - width + offset[1]), (0.5 + distance * width + offset[0], 2.5 + height * 2 - width + offset[1]))
        height = 1
        for width in range(distance // 2):
            # circuit_builder.rx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]))
            circuit_builder.ideal([(1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1])])

def surface_cnot_2(circuit_builder, distance , offset, rotation, tick):
    surface_rotate_x = rotation[0]
    surface_rotate_z = rotation[1]
    for height in range(distance - 1):
        for width in range(distance - 1):
            if (height + width) % 2 == 0:
                circuit_builder.cnot((1.5 + surface_rotate_z[tick][0] + width + offset[0], 1.5 + surface_rotate_z[tick][1] + height + offset[1]), (1.5 + width + offset[0], 1.5 + height + offset[1]))
            else:
                circuit_builder.cnot((1.5 + width + offset[0], 1.5 + height + offset[1]), (1.5 + surface_rotate_x[tick][0] + width + offset[0], 1.5 + surface_rotate_x[tick][1] + height + offset[1]))

    if tick == 2 or tick == 3:
        width = 0
        for height in range(distance // 2):
            # circuit_builder.rz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]))
            circuit_builder.ideal([(0.5 + width * distance + offset[0], 1.5 + height * 2 + width + offset[1])])
        width = 1
        for height in range(distance // 2):
            circuit_builder.cnot((0.5 + distance * width + surface_rotate_z[tick][0] + offset[0], 2.5 + surface_rotate_z[tick][1] + height * 2 - width + offset[1]), (0.5 + distance * width + offset[0], 2.5 + height * 2 - width + offset[1]))
        height = 1
        for width in range(distance // 2):
            # circuit_builder.rx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]))
            circuit_builder.ideal([(1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1])])

    if tick == 0 or tick == 1:
        width = 1
        for height in range(distance // 2):
            # circuit_builder.rz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]))
            circuit_builder.ideal([(0.5 + width * distance + offset[0], 1.5 + height * 2 + width + offset[1])])
        width = 0
        for height in range(distance // 2):
            circuit_builder.cnot((0.5 + distance * width + surface_rotate_z[tick][0] + offset[0], 2.5 + surface_rotate_z[tick][1] + height * 2 - width + offset[1]), (0.5 + distance * width + offset[0], 2.5 + height * 2 - width + offset[1]))
        height = 1
        for width in range(distance // 2):
            circuit_builder.cnot((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), (1.5 + surface_rotate_x[tick][0] + width * 2 + height + offset[0], 0.5 + height * distance + surface_rotate_x[tick][1] + offset[1]))

def surface_cnot_boundary(circuit_builder, distance , offset, rotation, tick):
    surface_rotate_x = rotation[0]
    surface_rotate_z = rotation[1]
    width = 0
    height = 0
    if tick == 0 or tick == 1:
        for width in range(distance // 2 - 1):
            # circuit_builder.rx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]))
            circuit_builder.ideal([(1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1])])
    if tick == 2 or tick == 3:
        for width in range(distance // 2 - 1):
            circuit_builder.cnot((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), (1.5 + surface_rotate_x[tick][0] + width * 2 + height + offset[0], 0.5 + height * distance + surface_rotate_x[tick][1] + offset[1]))

def surface_cnot_boundary_2(circuit_builder, distance , offset, rotation, tick):
    surface_rotate_x = rotation[0]
    surface_rotate_z = rotation[1]
    width = 0
    height = 0
    if tick == 0 or tick == 1:
        for width in range(distance // 2):
            # circuit_builder.rx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]))
            circuit_builder.ideal([(1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1])])
    if tick == 2 or tick == 3:
        for width in range(distance // 2):
            circuit_builder.cnot((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), (1.5 + surface_rotate_x[tick][0] + width * 2 + height + offset[0], 0.5 + height * distance + surface_rotate_x[tick][1] + offset[1]))

def surface_measurement_first(circuit_builder, distance , offset, tag):
    for height in range(distance - 1):
        for width in range(distance - 1):
            if (height + width) % 2 == 0:
                circuit_builder.mrz((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                tag += 1
            else:
                circuit_builder.mrx((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                circuit_builder.detector([-1], True, True)
                tag += 1
    for width in range(2):
        for height in range(distance // 2):
            circuit_builder.mrz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]), tag)
            tag += 1
    height = 1
    for width in range(distance // 2):
        circuit_builder.mrx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), tag)
        circuit_builder.detector([-1], True, True)
        tag += 1
    return tag
        
def surface_measurement(circuit_builder, distance , offset, tag):
    cnt = 0
    for height in range(distance - 1):
        for width in range(distance - 1):
            if (height + width) % 2 == 0:
                circuit_builder.mrz((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                if cnt in (6, 13, 15, 22):
                    circuit_builder.detector([-1, tag], True, False)
                else:
                    circuit_builder.detector([-1, tag], False, False)
                cnt += 1
                tag += 1
            else:
                circuit_builder.mrx((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                if cnt != 5:
                    if cnt in (7, 12, 14, 21, 23):
                        circuit_builder.detector([-1, tag], True, False)
                    else:
                        circuit_builder.detector([-1, tag], False, False)
                cnt += 1
                tag += 1
    for width in range(2):
        for height in range(distance // 2):
            circuit_builder.mrz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]), tag)
            if width == 1 and height <= 1:
                circuit_builder.detector([-1, tag], True, False)
            else:
                circuit_builder.detector([-1, tag], False, False)
            tag += 1
    for height in range(2):
        for width in range(distance // 2):
            if height == 0 and width == distance // 2 - 1:
                tag += 1
                continue
            circuit_builder.mrx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), tag)
            if height == 0 and width == distance // 2 - 2:
                circuit_builder.detector([-1, tag], True, False)
            else:
                circuit_builder.detector([-1, tag], False, False)
            tag += 1
    return tag
        
def surface_measurement_2(circuit_builder, distance , offset, tag):
    cnt = 0
    for height in range(distance - 1):
        for width in range(distance - 1):
            if (height + width) % 2 == 0:
                circuit_builder.mrz((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                if cnt in (6, 13, 15, 22):
                    circuit_builder.detector([-1, tag], True, False)
                else:
                    circuit_builder.detector([-1, tag], False, False)
                cnt += 1
                tag += 1
            else:
                circuit_builder.mrx((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                if cnt in (5, 7, 12, 14, 21, 23):
                    circuit_builder.detector([-1, tag], True, False)
                else:
                    circuit_builder.detector([-1, tag], False, False)
                cnt += 1
                tag += 1
    for width in range(2):
        for height in range(distance // 2):
            circuit_builder.mrz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]), tag)
            if width == 1 and height <= 1:
                circuit_builder.detector([-1, tag], True, False)
            else:
                circuit_builder.detector([-1, tag], False, False)
            tag += 1
    for height in range(2):
        for width in range(distance // 2):
            circuit_builder.mrx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), tag)
            if height == 0 and width == distance // 2 - 2:
                circuit_builder.detector([-1, tag], True, False)
            elif height == 0 and width == distance // 2 - 1:
                circuit_builder.detector([-1], True, False)
            else:
                circuit_builder.detector([-1, tag], False, False)
            tag += 1
    return tag

def surface_measurement_3(circuit_builder, distance , offset, tag):
    for height in range(distance - 1):
        for width in range(distance - 1):
            if (height + width) % 2 == 0:
                circuit_builder.mrz((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                circuit_builder.detector([-1, tag], False, False)
                tag += 1
            else:
                circuit_builder.mrx((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                circuit_builder.detector([-1, tag], False, False)
                tag += 1
    for width in range(2):
        for height in range(distance // 2):
            circuit_builder.mrz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]), tag)
            circuit_builder.detector([-1, tag], False, False)
            tag += 1
    for height in range(2):
        for width in range(distance // 2):
            circuit_builder.mrx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), tag)
            circuit_builder.detector([-1, tag], False, False)
            tag += 1
    return tag

def surface_data_initialization_expand(circuit_builder, distance, offset):
    distance_0 = 3
    for height in range(distance):
        if height < distance_0 - 1:
            for width in range(distance - distance_0):
                circuit_builder.rz((1 + width + offset[0], 1 + height + offset[1]))
        elif height == distance_0 - 1:
            for width in range(distance - distance_0):
                circuit_builder.rx((1 + width + offset[0], 1 + height + offset[1]))
        else:
            for width in range(distance):
                circuit_builder.rx((1 + width + offset[0], 1 + height + offset[1]))

def surface_ancilla_initialization_expand(circuit_builder, distance, offset):
    distance_0 = 3
    for height in range(distance - 1):
        for width in range(distance - 1):
            if (height == 0 and width > distance - distance_0 - 1) or (height == 1 and width > distance - distance_0 - 2) or (height == 2 and width > distance - distance_0):
                continue
            if (height + width) % 2 == 0:
                circuit_builder.rz((1.5 + width + offset[0], 1.5 + height + offset[1]))
            else:
                circuit_builder.rx((1.5 + width + offset[0], 1.5 + height + offset[1]))
    for width in range(2):
        for height in range(distance // 2):
            if width == 1 and height == 0:
                continue
            circuit_builder.rz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]))
    for height in range(2):
        for width in range(distance // 2):
            if height == 0 and width == distance // 2 - 1:
                continue
            circuit_builder.rx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]))

def surface_ancilla_initialization_expand_2(circuit_builder, distance, offset):
    for height in range(distance - 1):
        for width in range(distance - 1):
            if (height + width) % 2 == 0:
                circuit_builder.rz((1.5 + width + offset[0], 1.5 + height + offset[1]))
            else:
                circuit_builder.rx((1.5 + width + offset[0], 1.5 + height + offset[1]))
    for width in range(2):
        for height in range(distance // 2):
            if width == 1 and height == 0:
                continue
            circuit_builder.rz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]))
    for height in range(2):
        for width in range(distance // 2):
            if height == 0 and width == distance // 2:
                continue
            circuit_builder.rx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]))

def surface_measurement_first_expand(circuit_builder, distance, offset, tag):
    cnt = 0
    distance_0 = 3
    for height in range(distance - 1):
        for width in range(distance - 1):
            if (height + width) % 2 == 0:
                circuit_builder.mrz((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                if cnt in (0, 2, 4):
                    circuit_builder.detector([-1], False, False)
                cnt += 1
                tag += 1
            else:
                circuit_builder.mrx((1.5 + width + offset[0], 1.5 + height + offset[1]), tag)
                if cnt in (7, 14, 23):
                    circuit_builder.detector([-1], True, False)
                elif height >= 2:
                    circuit_builder.detector([-1], False, False)
                cnt += 1
                tag += 1
    for width in range(2):
        for height in range(distance // 2):
            circuit_builder.mrz((0.5 + width * distance + offset[0], 2.5 + height * 2 - width + offset[1]), tag)
            tag += 1
    for height in range(2):
        for width in range(distance // 2):
            if height == 0 and width == distance // 2 - 1:
                tag += 1
                continue
            circuit_builder.mrx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), tag)
            if height == 1:
                circuit_builder.detector([-1], False, False)
            tag += 1
    return tag

def surface_measurement_first_boundary_expand(circuit_builder, distance, offset, tag):
    height = 0
    for width in range(distance // 2 - 1):
        circuit_builder.mrx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), tag)
        tag += 1
    return tag

def surface_measurement_boundary_expand(circuit_builder, distance, offset, tag, postselect = False):
    height = 0
    for width in range(distance // 2):
        circuit_builder.mrx((1.5 + width * 2 + height + offset[0], 0.5 + height * distance + offset[1]), tag)
        if width != distance // 2 - 1:
            circuit_builder.detector([-1, tag], postselect, True)
        else:
            circuit_builder.detector([-1], postselect, True)
        tag += 1
    return tag

class RotatedBuilderProxy:
    def __init__(self, base_builder, center: tuple[float, float]):
        self._base = base_builder
        self._cx, self._cy = center

    def _rot(self, q: tuple[float, float]) -> tuple[float, float]:
        x, y = q
        dx = x - self._cx
        dy = y - self._cy
        return (self._cx + dy, self._cy - dx)

    def _map_arg(self, a: Any) -> Any:
        if isinstance(a, tuple) and len(a) == 2 and all(isinstance(v, (int, float)) for v in a):
            return self._rot(a)
        if isinstance(a, (list, tuple)):
            typ = type(a)
            return typ(self._map_arg(v) for v in a)
        return a

    def __getattr__(self, name: str):
        attr = getattr(self._base, name)
        if not callable(attr):
            return attr

        def wrapped(*args, **kwargs):
            new_args = [self._map_arg(a) for a in args]
            new_kwargs = {k: self._map_arg(v) for k, v in kwargs.items()}
            return attr(*new_args, **new_kwargs)
        return wrapped


def _rotation_center(distance: int, offset: tuple[float, float]) -> tuple[float, float]:
    cx = offset[0] + 1 + (distance - 1) / 2
    cy = offset[1] + 1 + (distance - 1) / 2
    return (cx, cy)

def surface_data_initialization_x_rot90(builder, distance, offset):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_data_initialization_x(proxy, distance, offset)

def surface_ancilla_initialization_x_rot90(builder, distance, offset):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_ancilla_initialization_x(proxy, distance, offset)

def surface_ancilla_initialization_x_boundary_rot90(builder, distance, offset):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_ancilla_initialization_x_boundary(proxy, distance, offset)

def surface_cnot_rot90(builder, distance, offset, rotation, tick):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_cnot(proxy, distance, offset, rotation, tick)

def surface_cnot_2_rot90(builder, distance, offset, rotation, tick):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_cnot_2(proxy, distance, offset, rotation, tick)

def surface_cnot_boundary_rot90(builder, distance, offset, rotation, tick):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_cnot_boundary(proxy, distance, offset, rotation, tick)

def surface_cnot_boundary_2_rot90(builder, distance, offset, rotation, tick):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_cnot_boundary_2(proxy, distance, offset, rotation, tick)

def surface_measurement_first_rot90(builder, distance, offset, tag):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_measurement_first(proxy, distance, offset, tag)

def surface_measurement_first_expand_rot90(builder, distance, offset, tag):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_measurement_first_expand(proxy, distance, offset, tag)

def surface_measurement_first_boundary_expand_rot90(builder, distance, offset, tag):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_measurement_first_boundary_expand(proxy, distance, offset, tag)

def surface_measurement_rot90(builder, distance, offset, tag):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_measurement(proxy, distance, offset, tag)

def surface_measurement_2_rot90(builder, distance, offset, tag):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_measurement_2(proxy, distance, offset, tag)

def surface_measurement_3_rot90(builder, distance, offset, tag):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_measurement_3(proxy, distance, offset, tag)

def surface_measurement_boundary_expand_rot90(builder, distance, offset, tag, postselect):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_measurement_boundary_expand(proxy, distance, offset, tag, postselect)

def surface_data_initialization_expand_rot90(builder, distance, offset):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_data_initialization_expand(proxy, distance, offset)

def surface_ancilla_initialization_expand_rot90(builder, distance, offset):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_ancilla_initialization_expand(proxy, distance, offset)

def surface_ancilla_initialization_expand_2_rot90(builder, distance, offset):
    proxy = RotatedBuilderProxy(builder, _rotation_center(distance, offset))
    return surface_ancilla_initialization_expand_2(proxy, distance, offset)

class MirrorUpDownBuilderProxy:
    def __init__(self, base_builder, center: tuple[float, float]):
        self._base = base_builder
        self._cx, self._cy = center

    def _mirror(self, q: tuple[float, float]) -> tuple[float, float]:
        x, y = q
        return (x, 2 * self._cy - y)

    def _map_arg(self, a: Any) -> Any:
        if isinstance(a, tuple) and len(a) == 2 and all(isinstance(v, (int, float)) for v in a):
            return self._mirror(a)
        if isinstance(a, (list, tuple)):
            typ = type(a)
            return typ(self._map_arg(v) for v in a)
        return a

    def __getattr__(self, name: str):
        attr = getattr(self._base, name)
        if not callable(attr):
            return attr

        def wrapped(*args, **kwargs):
            new_args = [self._map_arg(a) for a in args]
            new_kwargs = {k: self._map_arg(v) for k, v in kwargs.items()}
            return attr(*new_args, **new_kwargs)
        return wrapped


def _symmetry_center(distance: int, offset: tuple[float, float]) -> tuple[float, float]:
    cx = offset[0] + 1 + (distance - 1) / 2
    cy = offset[1] + 1 + (distance - 1) / 2
    return (cx, cy)

def surface_data_initialization_x_mirror_ud(builder, distance, offset):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_data_initialization_x(proxy, distance, offset)

def surface_ancilla_initialization_x_mirror_ud(builder, distance, offset):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_ancilla_initialization_x(proxy, distance, offset)

def surface_ancilla_initialization_x_boundary_mirror_ud(builder, distance, offset):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_ancilla_initialization_x_boundary(proxy, distance, offset)

def surface_cnot_mirror_ud(builder, distance, offset, rotation, tick):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_cnot(proxy, distance, offset, rotation, tick)

def surface_cnot_2_mirror_ud(builder, distance, offset, rotation, tick):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_cnot_2(proxy, distance, offset, rotation, tick)

def surface_cnot_boundary_mirror_ud(builder, distance, offset, rotation, tick):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_cnot_boundary(proxy, distance, offset, rotation, tick)

def surface_cnot_boundary_2_mirror_ud(builder, distance, offset, rotation, tick):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_cnot_boundary_2(proxy, distance, offset, rotation, tick)

def surface_measurement_first_mirror_ud(builder, distance, offset, tag):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_measurement_first(proxy, distance, offset, tag)

def surface_measurement_first_expand_mirror_ud(builder, distance, offset, tag):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_measurement_first_expand(proxy, distance, offset, tag)

def surface_measurement_first_boundary_expand_mirror_ud(builder, distance, offset, tag):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_measurement_first_boundary_expand(proxy, distance, offset, tag)

def surface_measurement_mirror_ud(builder, distance, offset, tag):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_measurement(proxy, distance, offset, tag)

def surface_measurement_2_mirror_ud(builder, distance, offset, tag):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_measurement_2(proxy, distance, offset, tag)

def surface_measurement_3_mirror_ud(builder, distance, offset, tag):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_measurement_3(proxy, distance, offset, tag)

def surface_measurement_boundary_expand_mirror_ud(builder, distance, offset, tag, postselect):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_measurement_boundary_expand(proxy, distance, offset, tag, postselect)

def surface_data_initialization_expand_mirror_ud(builder, distance, offset):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_data_initialization_expand(proxy, distance, offset)

def surface_ancilla_initialization_expand_mirror_ud(builder, distance, offset):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_ancilla_initialization_expand(proxy, distance, offset)

def surface_ancilla_initialization_expand_2_mirror_ud(builder, distance, offset):
    proxy = MirrorUpDownBuilderProxy(builder, _symmetry_center(distance, offset))
    return surface_ancilla_initialization_expand_2(proxy, distance, offset)
