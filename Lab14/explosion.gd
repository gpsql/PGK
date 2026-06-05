extends Node3D

## Scena jednorazowej eksplozji cząsteczkowej.
## Instancjonowana przez bossa (i opcjonalnie przez wrogów) w chwili śmierci.
## Uruchamia cząsteczki i usuwa się sama po wygaśnięciu efektu.

const AUTO_FREE_DELAY: float = 0.8   # sekundy do usunięcia po emisji

func _ready() -> void:
	$GPUParticles3D.emitting = true
	await get_tree().create_timer(AUTO_FREE_DELAY).timeout
	queue_free()
