extends Node3D

## Główny skrypt sceny Lab 11.
## Należy do grupy "score_tracker" — WaveSpawner wywołuje add_score() przez grupę.

var score: int = 0


func _ready() -> void:
	add_to_group("score_tracker")


func add_score(points: int) -> void:
	score += points
	print("=== WYNIK: %d ===" % score)
