from django.shortcuts import render

# Create your views here.


data_members = [{'position': 'Team leader', 'name': 'Adil Gumarov', 'ph_num': '+7 (777) 129 57-47', 'ph_num_href': '+77771295747', 'off_hours': '08:00 - 16:00', 'pic_src': 'movies/images/adil.jpeg'},
                {'position': 'Developer',   'name': 'Dias Kabenov', 'ph_num': '+7 (708) 105 88-62', 'ph_num_href': '+77081058862', 'off_hours': '09:00 - 17:00', 'pic_src': 'movies/images/dias.jpeg'}
]

data_team = [{'name': 'Adil Gumarov', 'group': 'ITSE-1902', 'course': '3rd course', 'pic_src': 'movies/images/team_member-1.jpg'},
             {'name': 'Dias Kabenov', 'group': 'ITSE-1902', 'course': '3rd course', 'pic_src': 'movies/images/team_member-2.jpg'}
]


def about_project(request):
    return render(request, 'movies/about_project.html', {'title': 'About project'})


def about_team(request):
    return render(request, 'movies/about_team.html', {'title': 'About team', 'members_data': data_team})


def dev_contacts(request):
    return render(request, 'movies/dev_contacts.html', {'title': 'Dev contacts', 'members_data': data_members})