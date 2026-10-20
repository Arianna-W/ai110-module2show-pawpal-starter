def format_task_name(name: str) -> str:
	"""Add a care-type icon based on common task-name keywords."""
	normalized_name = name.casefold()
	icon_by_keywords = (
		(("med",), "💊"),
		(("walk",), "🚶"),
		(("feed", "meal", "breakfast", "dinner"), "🍽️"),
		(("groom", "brush", "bath"), "🧼"),
		(("play", "enrich"), "🎾"),
	)
	icon = next(
		(
			icon
			for keywords, icon in icon_by_keywords
			if any(keyword in normalized_name for keyword in keywords)
		),
		"🐾",
	)
	return f"{icon} {name}"


def format_priority(priority_level: str) -> str:
	"""Return a color-coded display label for a task priority."""
	icon = {
		"low": "🟢",
		"medium": "🟡",
		"high": "🔴",
	}.get(priority_level.casefold(), "⚪")
	return f"{icon} {priority_level}"


def format_status(completed: bool) -> str:
	"""Return a visual status label for a task."""
	return "✅ Completed" if completed else "🟠 To do"