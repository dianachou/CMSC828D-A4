try:
    import simplejson as json
except ImportError:
    import json
from flask import Flask, request, Response, render_template, jsonify
import psycopg2  # use this package to work with postgresql
from psycopg2 import sql
import pprint
import datetime

app = Flask(__name__)

conn_string = "host='localhost' dbname='a3database' user='cmsc828d'"
print("Connecting to database\n	->%s" % (conn_string))

conn = psycopg2.connect("host='localhost' dbname='a3database' user='cmsc828d'")
print("Connected!\n")

def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)


################################# PAGE ROUTES #################################
@app.route('/')
def renderPage():
    return render_template("index.html")

@app.route('/a2')
def renderA2():
    return render_template("a2.html")

################################# JSON ROUTES #################################
@app.route("/get-server-data")
def get_server_data():
    event_arg = request.args.get('event')
    timestamp_arg = request.args.get('timestamp')
    interaction_log = {"event": event_arg, "timestamp": timestamp_arg}

    # if event is brushing, then don't print logs!
    if (event_arg != 'brush'):
        append_new_line('logs.txt', str(interaction_log))

    cursor = conn.cursor()
    schema_name = request.args.get('schema')
    table_name = request.args.get('table')

    query = "SELECT MIN(date), MAX(date) FROM {s}.{t}"
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
    ))
    records = cursor.fetchall()
    date_range = [dict(zip(["min","max"], rows)) for rows in records]

    if (event_arg == "initialize"):
        datemin_arg = date_range[0]['min']
        datemax_arg = date_range[0]['max']
    else:
        datemin_arg = request.args.get('date-min')
        datemax_arg = request.args.get('date-max')

    filter_arg = json.loads(request.args.get('filter-data'))

    race = filter_arg.get('race', [])
    age = filter_arg.get('age_group', [])
    gender = filter_arg.get('gender', [])
    flee = filter_arg.get('flee', [])
    body_cam = filter_arg.get('body_camera', [])
    body_cam = [True if x == "true" else False for x in body_cam]
    mental_ill = filter_arg.get('signs_of_mental_illness', [])
    mental_ill = [True if x == "true" else False for x in mental_ill]

    query = "SELECT * FROM {s}.{t} LIMIT 0"
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name)
    ))    
    attributes = [desc[0] for desc in cursor.description]

    # Loads the GeoJSON file to create the chloropleth map
    geo_data = json.load(open('data/us-states.json'))

    # Dictionary for storing the full names of each state
    us_state_abbr = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
        'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia',
        'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky',
        'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
        'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska',
        'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
        'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'PW': 'Palau', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia',
        'VI': 'Virgin Islands', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    # print(geo_data)

    query = """
        SELECT COUNT(*) FROM {s}.{t}
        WHERE date BETWEEN {d_min}::DATE AND {d_max}::DATE
            AND race = ANY({r})
            AND age_group = ANY({ag}) 
            AND gender = ANY({g}) 
            AND flee = ANY({f})
            AND body_camera = ANY({bc})
            AND signs_of_mental_illness = ANY({smi})
    """
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
        d_min=sql.Literal(datemin_arg), d_max=sql.Literal(datemax_arg),
        r=sql.Literal(race), ag=sql.Literal(age), g=sql.Literal(gender),
        f=sql.Literal(flee), bc=sql.Literal(body_cam), smi=sql.Literal(mental_ill),
    ))
    records = cursor.fetchall()
    total_query = [dict(zip(["count"], rows)) for rows in records]

    query = """
        SELECT state, COUNT(*) AS cnt FROM {s}.{t}
        WHERE date BETWEEN {d_min}::DATE AND {d_max}::DATE
            AND race = ANY({r})
            AND age_group = ANY({ag}) 
            AND gender = ANY({g}) 
            AND flee = ANY({f})
            AND body_camera = ANY({bc})
            AND signs_of_mental_illness = ANY({smi})
        GROUP BY state 
        ORDER BY cnt ASC 
    """
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
        d_min=sql.Literal(datemin_arg), d_max=sql.Literal(datemax_arg),
        r=sql.Literal(race), ag=sql.Literal(age), g=sql.Literal(gender),
        f=sql.Literal(flee), bc=sql.Literal(body_cam), smi=sql.Literal(mental_ill),
    ))
    records = cursor.fetchall()
    state_count_query = [dict(zip(["state","count"], (us_state_abbr[rows[0]], rows[1]))) for rows in records]
    state_domain = [rows[1] for rows in records]

    months = []
    date_ranges = []
    date_count = []
    dates = {}
    if (schema_name == "a3"):
        # Use Materialized View for A3
        query = "SELECT * FROM a3.month_year_count_matview;"
        cursor.execute(sql.SQL(query))
    else:
        # Use Table for A2
        query = """
                SELECT 
                    EXTRACT(MONTH FROM date)::INT AS month, 
                    EXTRACT(YEAR FROM date)::INT AS year, 
                    COUNT(*)
                FROM {s}.{t}
                GROUP BY month, year
                ORDER BY year, month
            """
        cursor.execute(sql.SQL(query).format(
            s=sql.Identifier(schema_name),
            t=sql.Identifier(table_name),
            d_min=sql.Literal(datemin_arg),
            d_max=sql.Literal(datemax_arg),
        ))
    records = cursor.fetchall()
    for i, row in enumerate(records):
        date = str(datetime.date(row[1], row[0], 1))

        if date not in dates:
            dates[date] = {"date": date}
        dates[date]["count"] = row[2]
        date_count.append(row[2])
        year = row[1]
        month = row[0]
        d = str(datetime.date(year, month, 1))
        months.append(d)

        if i == len(records) - 1:
            if month == 12:
                month = 0
            months.append(str(datetime.date(year, month+1, 1)))

    for i in range(len(months) - 1):
        date_ranges.append({'rangeMin': months[i], 'rangeMax': months[i + 1]})

    query = """
        SELECT race, COUNT(*) AS cnt FROM {s}.{t}
        WHERE date BETWEEN {d_min}::DATE AND {d_max}::DATE
            AND race = ANY({r})
            AND age_group = ANY({ag}) 
            AND gender = ANY({g}) 
            AND flee = ANY({f})
            AND body_camera = ANY({bc})
            AND signs_of_mental_illness = ANY({smi})
        GROUP BY race 
        ORDER BY cnt DESC 
    """
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
        d_min=sql.Literal(datemin_arg), d_max=sql.Literal(datemax_arg),
        r=sql.Literal(race), ag=sql.Literal(age), g=sql.Literal(gender),
        f=sql.Literal(flee), bc=sql.Literal(body_cam), smi=sql.Literal(mental_ill)
    ))
    records = cursor.fetchall()
    race_query = [dict(zip(["race", "count"], rows)) for rows in records]

    query = """
        SELECT age_group, COUNT(*) AS cnt FROM {s}.{t}
        WHERE date BETWEEN {d_min}::DATE AND {d_max}::DATE
            AND race = ANY({r})
            AND age_group = ANY({ag}) 
            AND gender = ANY({g}) 
            AND flee = ANY({f})
            AND body_camera = ANY({bc})
            AND signs_of_mental_illness = ANY({smi})
        GROUP BY age_group 
        ORDER BY cnt DESC 
    """
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
        d_min=sql.Literal(datemin_arg), d_max=sql.Literal(datemax_arg),
        r=sql.Literal(race), ag=sql.Literal(age), g=sql.Literal(gender),
        f=sql.Literal(flee), bc=sql.Literal(body_cam), smi=sql.Literal(mental_ill)
    ))
    records = cursor.fetchall()
    age_group_query = [dict(zip(["age_group", "count"], rows)) for rows in records]

    query = """
        SELECT body_camera, COUNT(*) AS cnt FROM {s}.{t}
        WHERE date BETWEEN {d_min}::DATE AND {d_max}::DATE
            AND race = ANY({r})
            AND age_group = ANY({ag}) 
            AND gender = ANY({g}) 
            AND flee = ANY({f})
            AND body_camera = ANY({bc})
            AND signs_of_mental_illness = ANY({smi})
        GROUP BY body_camera 
        ORDER BY cnt DESC 
    """
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
        d_min=sql.Literal(datemin_arg), d_max=sql.Literal(datemax_arg),
        r=sql.Literal(race), ag=sql.Literal(age), g=sql.Literal(gender),
        f=sql.Literal(flee), bc=sql.Literal(body_cam), smi=sql.Literal(mental_ill)
    ))
    records = cursor.fetchall()
    body_camera_query = [dict(zip(["body_camera", "count"], rows)) for rows in records]

    query = """
        SELECT signs_of_mental_illness, COUNT(*) AS cnt FROM {s}.{t}
        WHERE date BETWEEN {d_min}::DATE AND {d_max}::DATE
            AND race = ANY({r})
            AND age_group = ANY({ag}) 
            AND gender = ANY({g}) 
            AND flee = ANY({f})
            AND body_camera = ANY({bc})
            AND signs_of_mental_illness = ANY({smi})
        GROUP BY signs_of_mental_illness 
        ORDER BY cnt DESC 
    """
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
        d_min=sql.Literal(datemin_arg), d_max=sql.Literal(datemax_arg),
        r=sql.Literal(race), ag=sql.Literal(age), g=sql.Literal(gender),
        f=sql.Literal(flee), bc=sql.Literal(body_cam), smi=sql.Literal(mental_ill)
    ))
    records = cursor.fetchall()
    signs_of_mental_illness_query = [dict(zip(["signs_of_mental_illness", "count"], rows)) for rows in records]

    query = """
        SELECT flee, COUNT(*) AS cnt FROM {s}.{t}
        WHERE date BETWEEN {d_min}::DATE AND {d_max}::DATE
            AND race = ANY({r})
            AND age_group = ANY({ag}) 
            AND gender = ANY({g}) 
            AND flee = ANY({f})
            AND body_camera = ANY({bc})
            AND signs_of_mental_illness = ANY({smi})
        GROUP BY flee 
        ORDER BY cnt DESC 
    """
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
        d_min=sql.Literal(datemin_arg), d_max=sql.Literal(datemax_arg),
        r=sql.Literal(race), ag=sql.Literal(age), g=sql.Literal(gender),
        f=sql.Literal(flee), bc=sql.Literal(body_cam), smi=sql.Literal(mental_ill)
    ))
    records = cursor.fetchall()
    flee_query = [dict(zip(["flee", "count"], rows)) for rows in records]

    query = """
        SELECT gender, COUNT(*) AS cnt FROM {s}.{t}
        WHERE date BETWEEN {d_min}::DATE AND {d_max}::DATE
            AND race = ANY({r})
            AND age_group = ANY({ag}) 
            AND gender = ANY({g}) 
            AND flee = ANY({f})
            AND body_camera = ANY({bc})
            AND signs_of_mental_illness = ANY({smi})
        GROUP BY gender 
        ORDER BY cnt DESC 
    """
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
        d_min=sql.Literal(datemin_arg), d_max=sql.Literal(datemax_arg),
        r=sql.Literal(race), ag=sql.Literal(age), g=sql.Literal(gender),
        f=sql.Literal(flee), bc=sql.Literal(body_cam), smi=sql.Literal(mental_ill)
    ))
    records = cursor.fetchall()
    gender_query = [dict(zip(["gender", "count"], rows)) for rows in records]

    query = """
        SELECT COUNT(*) FROM {s}.{t}
        WHERE date BETWEEN {d_min}::DATE AND {d_max}::DATE
            AND race = ANY({r})
            AND age_group = ANY({ag}) 
            AND gender = ANY({g}) 
            AND flee = ANY({f})
            AND body_camera = ANY({bc})
            AND signs_of_mental_illness = ANY({smi})
    """
    cursor.execute(sql.SQL(query).format(
        s=sql.Identifier(schema_name),
        t=sql.Identifier(table_name),
        d_min=sql.Literal(datemin_arg), d_max=sql.Literal(datemax_arg),
        r=sql.Literal(race), ag=sql.Literal(age), g=sql.Literal(gender),
        f=sql.Literal(flee), bc=sql.Literal(body_cam), smi=sql.Literal(mental_ill)
    ))
    records = cursor.fetchall()
    max_count = [dict(zip(["total", "count"], rows)) for rows in records]

    if state_count_query == []:
        state_count_query = [{'state': '', 'count': 0}]

    #################### DATA FOR RESPONSE ####################

    data = {
        "geoJSON": geo_data,
        "attributes": attributes,
        "totalShootings" : total_query,
        "stateDomain": state_domain,
        "countPerState": state_count_query,
        "properties": {
            "shootingsPerMonth": list(dates.values()),
            "dateBinRange": date_ranges,
            "dateBinCount": date_count,
            "dateMin": str(datemin_arg),
            "dateMax": str(datemax_arg),
            "stateMin": state_count_query[0]['count'],
            "stateMax": state_count_query[len(state_count_query)-1]['count']
        },
        "barCounts": {
            "race": race_query,
            "gender": gender_query,
            "age": age_group_query,
            "bodyCamera": body_camera_query,
            "mentalIllness": signs_of_mental_illness_query,
            "flee": flee_query,
            "maxCount": max_count
        }
    }

    cursor.close()
    resp = Response(response=json.dumps(data), status=200, mimetype='application/json')
    h = resp.headers
    h['Access-Control-Allow-Origin'] = "*"
    return resp

################################# START SERVER ################################
if __name__ == "__main__":
    app.run(debug=False, port=8000)
