extends Node3D

## Statyczny cel do zestrzelenia.
## Należy do grupy "targets" — główna scena podłącza sygnały przez grupę.
## Area3D na Layer 2, maska 4 — wykrywa pociski gracza (Layer 3).

signal destroyed

var _hit: bool = false


func _ready() -> void:
	add_to_group("targets")
	$Area3D.area_entered.connect(_on_hit)


func _on_hit(_area: Area3D) -> void:
	if _hit:
		return
	_hit = true
	print("Cel trafiony!")

	# Zadanie *: czerwony błysk przed usunięciem
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(1.0, 0.1, 0.0, 1.0)
	mat.emission_enabled = true
	mat.emission = Color(1.0, 0.0, 0.0, 1.0)
	mat.emission_energy_multiplier = 4.0
	$MeshInstance3D.set_surface_override_material(0, mat)

	emit_signal("destroyed")
	await get_tree().create_timer(0.12).timeout
	queue_free()
