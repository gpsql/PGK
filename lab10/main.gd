extends Node3D

## Główny skrypt sceny Lab 10.
## Śledzi wynik i podłącza sygnały celów.

var score: int = 0


func _ready() -> void:
	# Podłącz sygnał "destroyed" do każdego celu istniejącego w scenie
	for target in get_tree().get_nodes_in_group("targets"):
		target.destroyed.connect(_on_target_destroyed)


func _on_target_destroyed() -> void:
	score += 1
	print("Wynik: %d" % score)
