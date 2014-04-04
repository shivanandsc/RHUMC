"""
    Conference scheduling software for undergraduate institutions.
    Created specifically for the Mathematics department of the
    Rose-Hulman Institute of Technology (http://www.rose-hulman.edu/math.aspx).
    
    Copyright (C) 2013-2014  Nick Crawford <crawfonw -at- gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from django.contrib import admin

from models import Attendee, Conference, Contactee, Page, Room, Track, Day, TimeSlot, Session, SpecialSession

class FengShuiAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_per_page = 50
    
class AttendeeAdmin(FengShuiAdmin):
    fieldsets = (
                  ('General Information', {
                          'fields': ('conference', 'first_name', 'last_name', 'email', 'sex',),
                          }),
                  ('School Information', {
                                          'classes': ('collapse',),
                                          'fields': ('school', 'size_of_institute', 'attendee_type', 'year',),
                                          }),
                  ('Talk Information', {
                                        'classes': ('collapse',),
                                        'fields': ('is_submitting_talk', 'paper_title', 'paper_abstract', 'is_submitted_for_best_of_competition',),
                                        }),
                  ('Miscellaneous', {
                                     'classes': ('collapse',),
                                     'fields': ('dietary_restrictions', 'requires_housing', 'has_been_paired_for_housing', 'comments',),
                                     })
                  
                  )
    list_display = ('__unicode__', 'school', 'attendee_type', 'is_submitting_talk', 'requires_housing', 'has_been_paired_for_housing', 'conference',)
    list_filter = ('attendee_type', 'is_submitting_talk', 'requires_housing', 'has_been_paired_for_housing', 'conference',)
    search_fields = ('first_name', 'last_name', 'school', 'paper_title', 'paper_abstract', 'dietary_restrictions', 'comments',)
    actions = ('pair_for_housing', 'unpair_for_housing',)
    
    def pair_for_housing(self, request, queryset):
        queryset.update(has_been_paired_for_housing=True)
    pair_for_housing.short_description = 'Pair selected contactees for housing'

    def unpair_for_housing(self, request, queryset):
        queryset.update(has_been_paired_for_housing=False)
    unpair_for_housing.short_description = 'Unpair selected contactees for housing'

class PageAdmin(FengShuiAdmin):
    fieldsets = (
                  ('General Settings', {
                                        'fields': ('title',),
                                        }),
                  ('Link Settings', {
                                     'fields': ('is_link', 'link',),
                                    }),
                  ('Page Settings', {
                                    'fields': ('on_sidebar', 'page_text',),
                                    }),
                  )

class ConferenceAdmin(FengShuiAdmin):
    list_display = ('name', 'start_date', 'end_date', 'registration_open', 'past_conference',)
    list_filter = ('registration_open',)
    search_fields = ('name',)
    
class SessionAdmin(FengShuiAdmin):
    filter_horizontal = ('speakers',)
    list_display = ('day', 'time', 'track', 'chair',)
    
class ContacteeAdmin(FengShuiAdmin):
    list_display = ('name', 'active_contact',)
    actions = ('toggle_active_concatee',)
    
    def toggle_active_concatee(self, request, queryset):
        updated = 0
        for contactee in queryset:
            contactee.active_contact=(not contactee.active_contact)
            contactee.save()
            updated += 1
        if updated == 1:
            msg = '1 contactee'
        else:
            msg = '%s contactees' % updated
        self.message_user(request, '%s active state successfully toggled.' % msg)
    toggle_active_concatee.short_description = 'Toggle active state for selected contactees'
    
class TrackAdmin(FengShuiAdmin):
    list_display = ('name', 'room', 'conference',)
    
class DayAdmin(FengShuiAdmin):
    list_display = ('date', 'conference',)
    
class SpecialSessionAdmin(FengShuiAdmin):
    list_display = ('day', 'room', 'speaker',)

admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Contactee, ContacteeAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Room)
admin.site.register(Track, TrackAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(SpecialSession, SpecialSessionAdmin)
admin.site.register(TimeSlot)