extends Node3D

## Spawner fal wrogów — wzorzec data-driven.
## Kod spawnera jest generyczny; dane fal definiują wszystko.
## Dlaczego wrogowie trafiają do root, nie do PathFollow3D?
## — bo wróg ma stać w globalnej przestrzeni i nie jechać z szyną.

@export var enemy_scene: PackedScene
@export var enemy_bullet_scene: PackedScene

# -----------------------------------------------------------------------
# Dane fal: każdy słownik to jedna fala.
# "delay"       — ile sekund od startu gry czekamy na spawn tej fali
# "x_positions" — pozycje X kolejnych wrogów (względem osi szyny)
# "z_offset"    — przesunięcie Z przed kamerą (wartość ujemna = do przodu)
# -----------------------------------------------------------------------
var _waves: Array[Dictionary] = [
	{ "delay":  2.0, "x_positions": [ 0.0],              "z_offset": -18.0 },
	{ "delay":  7.0, "x_positions": [-3.0, 3.0],          "z_offset": -22.0 },
	{ "delay": 13.0, "x_positions": [-4.0, 0.0, 4.0],     "z_offset": -20.0 },
	{ "delay": 20.0, "x_positions": [-3.5, -1.2, 1.2, 3.5], "z_offset": -24.0 },
	{ "delay": 28.0, "x_positions": [-2.0, 0.0, 2.0],     "z_offset": -26.0 },
]

var _spawned: Array[bool] = []
var _time: float = 0.0


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
	# Baza pozycji = bieżące miejsce PathFollow3D na szynie
	var rail_nodes := get_tree().get_nodes_in_group("rail")
	var base_pos := Vector3.ZERO
	if not rail_nodes.is_empty():
		base_pos = rail_nodes[0].global_position

	var positions: Array = wave["x_positions"]
	for j in positions.size():
		if enemy_scene == null:
			push_warning("WaveSpawner: enemy_scene nie ustawione!")
			return

		var enemy: Node3D = enemy_scene.instantiate()
		# Przypisz scenę pocisku przed dodaniem do drzewa
		enemy.enemy_bullet_scene = enemy_bullet_scene
		get_tree().root.add_child(enemy)
		enemy.global_position = base_pos + Vector3(positions[j], 0.0, wave["z_offset"])

	print("Fala spawned: %d wrogów" % positions.size())

