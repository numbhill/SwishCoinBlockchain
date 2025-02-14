from django.contrib import admin
from .models import UserProfile, Question, Answer, Transaction, Block


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)
    actions = ["increase_balance", "decrease_balance"]

    def increase_balance(self, request, queryset):
        if request.user.is_superuser:
            for profile in queryset:
                if UserProfile.can_create_new_coins(500):
                    profile.balance += 500
                    profile.save()
            self.message_user(request, "Balance increased successfully.")
        else:
            self.message_user(request, "Permission denied.", level="error")

    def decrease_balance(self, request, queryset):
        if request.user.is_superuser:
            for profile in queryset:
                if profile.balance >= 500:
                    profile.balance -= 500
                    profile.save()
            self.message_user(request, "Balance decreased successfully.")
        else:
            self.message_user(request, "Permission denied.", level="error")

    increase_balance.short_description = "Increase balance by 500 SwishCoins"
    decrease_balance.short_description = "Decrease balance by 500 SwishCoins"


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'bounty', 'created_at')
    search_fields = ('title', 'user__username')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'votes', 'created_at')
    search_fields = ('question__title', 'user__username')


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
    "sender", "receiver", "amount", "timestamp", "transaction_type")  # ✅ Replace mined with transaction_type
    list_filter = ("transaction_type",)  # ✅ Use transaction_type instead of mined


class BlockAdmin(admin.ModelAdmin):
    list_display = ('previous_hash', 'timestamp', 'nonce', 'hash')


# ✅ Register models only once
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Transaction, TransactionAdmin)  # ✅ Ensure this is only registered once
admin.site.register(Block, BlockAdmin)
