from django import forms
from .models import Task, Category, Team

class TaskForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'step': '1'  # Enable seconds in the datetime picker
        }),
        input_formats=['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M'],  # Support both with and without seconds
        required=False,
        help_text='Optional: Manually set start time (leave empty to use stopwatch)'
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'step': '1'  # Enable seconds in the datetime picker
        }),
        input_formats=['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M'],  # Support both with and without seconds
        required=False,
        help_text='Optional: Manually set end time (leave empty to use stopwatch)'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'start_time', 'end_time']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, team=None, **kwargs):
        self.team = team  # Store team as instance variable
        super().__init__(*args, **kwargs)
        if team:
            self.fields['category'].queryset = Category.objects.filter(team=team)
        else:
            self.fields['category'].queryset = Category.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        category = cleaned_data.get('category')

        if end_time and not start_time:
            raise forms.ValidationError('Start time must be set if end time is set')
        
        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError('End time must be after start time')

        # Validate category belongs to the correct team
        if category and self.team and category.team_id != self.team.id:
            raise forms.ValidationError({
                'category': f'Selected category (team {category.team_id}) does not belong to the correct team ({self.team.id})'
            })

        # Set status based on times
        if start_time and end_time:
            cleaned_data['status'] = 'completed'
        elif start_time:
            cleaned_data['status'] = 'in_progress'
        else:
            cleaned_data['status'] = 'not_started'

        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
