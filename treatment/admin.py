from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from treatment.models import (
    BodySection,
    Difficulty,
    Equipment,
    Exercise,
    ExerciseType,
    Expertise,
    Regime,
)

admin.site.register(Difficulty, SimpleHistoryAdmin)
admin.site.register(Expertise, SimpleHistoryAdmin)
admin.site.register(ExerciseType, SimpleHistoryAdmin)
admin.site.register(BodySection, SimpleHistoryAdmin)
admin.site.register(Exercise, SimpleHistoryAdmin)
admin.site.register(Regime, SimpleHistoryAdmin)
admin.site.register(Equipment, SimpleHistoryAdmin)
