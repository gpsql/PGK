extends Node3D

## Spawner fal wrogów — wzorzec data-driven.
## Kod spawnera jest generyczny; dane fal definiują wszystko.
## Dlaczego wrogowie trafiają do root, nie do PathFollow3D?
## — bo wróg ma stać w globalnej przestrzeni i nie jechać z szyną.

@export var enemy_scene:        PackedScene
@export var enemy_bullet_scene: PackedScene
@export var explosion_scene:    PackedScene   # przekazywane wrogom przy spawnie

# -----------------------------------------------------------------------
# Dane fal: każdy słownik to jedna fala.
# [REFAKTORYZACJA: magic-numbers] offsety fal opisane słownikowo, nie inline
# "delay"       — ile sekund od startu gry czekamy na spawn tej fali
# "x_positions" — pozycje X kolejnych wrogów (względem osi szyny)
# "z_offset"    — przesunięcie Z przed kamerą (wartość ujemna = do przodu)
# -----------------------------------------------------------------------
var _waves: Array[Dictionary] = [
	{ "delay":  2.0, "x_positions": [ 0.0],                 "z_offset": -18.0 },
	{ "delay":  7.0, "x_positions": [-3.0, 3.0],            "z_offset": -22.0 },
	{ "delay": 13.0, "x_positions": [-4.0, 0.0, 4.0],       "z_offset": -20.0 },
	{ "delay": 20.0, "x_positions": [-3.5, -1.2, 1.2, 3.5], "z_offset": -24.0 },
	{ "delay": 28.0, "x_positions": [-2.0, 0.0, 2.0],       "z_offset": -26.0 },
]

var _spawned: Array[bool] = []
var _time:    float       = 0.0


func _ready() -> void:
	_spawned.resize(_waves.size())
	_spawned.fill(false)


func _process(delta: float) -> void:
	_time += delta
	for i in _waves.size():
		if _spawned[i]:
			continue
		if _time >= _waves[i]["delay"]:
			_spawn_wave(_waves[i])
			_spawned[i] = true


func _spawn_wave(wave: Dictionary) -> void:
	var rail_nodes := get_tree().get_nodes_in_group("rail")
	var base_pos: Vector3 = Vector3.ZERO
	if not rail_nodes.is_empty():
		var rail_node := rail_nodes[0] as Node3D
		if rail_node != null:
			base_pos = rail_node.global_position

	var positions: Array = wave["x_positions"]
	for j in positions.size():
		# [REFAKTORYZACJA: long-methods] logika tworzenia wroga wydzielona do _create_enemy_at()
		_create_enemy_at(base_pos + Vector3(positions[j], 0.0, wave["z_offset"]))

	print("Fala spawned: %d wrogów" % positions.size())


## Pomocnik tworzenia pojedynczego wroga — wydzielony z _spawn_wave().
## [REFAKTORYZACJA: duplicate-code] jedno miejsce dla logiki konfiguracji instancji wroga.
func _create_enemy_at(pos: Vector3) -> void:
	if enemy_scene == null:
		push_warning("WaveSpawner: enemy_scene nie ustawione!")
		return
	var enemy: Node3D = enemy_scene.instantiate()
	enemy.enemy_bullet_scene = enemy_bullet_scene
	enemy.explosion_scene    = explosion_scene
	get_tree().root.add_child(enemy)
	enemy.global_position = pos
