from flask import (flash, make_response, redirect, render_template, request,
                   url_for)

from ..main import main
from ..auth import auth
from ..posts import posts

@main.route('/')
def welcomePage():
    return render_template('splash.html')


@main.route('/location')
def locationPage():
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
              'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
              'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
              'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
              'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
              'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
              'New York', 'North Carolina', 'North Dakota',
              'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode',
              'Island', 'South', 'Carolina', 'South', 'Dakota', 'Tennessee',
              'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
              'Wisconsin', 'Wyoming'
              ]

    return render_template('map.html', states=states)
