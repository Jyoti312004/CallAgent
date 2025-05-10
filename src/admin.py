from django.contrib import admin
from src.models import User, QueryRequest, KnowledgeBase

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at", "updated_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 10
    date_hierarchy = "created_at"

@admin.register(QueryRequest)
class QueryRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "status", "created_at", "updated_at")
    search_fields = ("question",)
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
    list_per_page = 10
    date_hierarchy = "created_at"

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer", "type", "source", "created_at", "updated_at")
    search_fields = ("question", "answer")
    list_filter = ("type", "source", "created_at")
    ordering = ("-created_at",)
    list_per_page = 10
    date_hierarchy = "created_at"