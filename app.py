from flask import Flask, render_template,request
import matplotlib.pyplot as plt
import ternary
from matplotlib.patches import Polygon


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['GET','POST'])
def tex_calculate():

    sand = float(request.form.get('Sand'))
    clay = float(request.form.get('Clay'))
    silt = (100-(sand+clay))

    #Making a ternary graph
    figure, tax = ternary.figure(scale=100)
    tax.boundary(linewidth=2.0)
    tax.gridlines(color="black", multiple=10)

    #Assigning the names to the labels
    tax.right_axis_label("Silt (%)", fontsize=14, offset=0.18)
    tax.left_axis_label("Clay (%)", fontsize=14, offset=0.18)
    tax.bottom_axis_label("Sand (%)", fontsize=14, offset=0.18)

    # Plot a marker at the intersection point using ternary graph
    point = tax.plot([(silt,clay)],marker='o', color='blue')

    #Defining the soil regions
    regions = {
        "Sand": [(0, 0), (15, 0),(5, 8.660254038)],
        "Loamy Sand": [(5, 8.660254038), (7.5, 12.99038106),(30, 0),(15,0)],
        "Sandy Loam": [(7.5, 12.99038106),(10,17.32050808 ),(37.5, 17.32050808), (43.75,6.495190528),(53.75, 6.495190528), (50, 0), (30, 0)],
        "Sandy Clay Loam": [(37.5, 17.32050808), (10, 17.32050808),(17.5, 30.31088913), (37.5,30.31088913), (41.25,23.8156986)],
        "Sandy Clay": [(37.5, 30.31088913), (17.5, 30.31088913),(27.5, 47.63139721)],
        "Clay": [(27.5, 47.63139721), (35, 34.64101615),(60, 34.64101615), (70,51.96152423), (50,86.60254038)],
        "Clay Loam": [(35, 34.64101615), (60, 34.64101615),(66.25, 23.8156986), (41.25, 23.8156986)],
        "Loam": [(37.5, 17.32050808), (43.75, 6.495190528),(53.75, 6.495190528), (63.75, 23.8156986), (41.25, 23.8156986)],
        "Silty Clay": [(60, 34.64101615), (80, 34.64101615),(70, 51.96152423)],
        "Silt Clay Loam": [(60, 34.64101615), (80, 34.64101615),(86.25, 23.8156986),(66.25, 23.8156986)],
        "Silt Loam": [(86.25, 23.8156986),(63.75, 23.8156986), (50,0),(80,0),(86.25, 10.82531755), (93.75, 10.82531755)],
        "Silt": [(86.25, 10.82531755), (93.75, 10.82531755),(100, 0),(80, 0)],
    }

    # Showing the regions and their name
    for region_name, vertices in regions.items():
        polygon = Polygon(vertices, closed=True, edgecolor='black',linewidth = 1.5, facecolor='white')
        ternary.plt.gca().add_patch(polygon)

        # Calculate the centroid of the polygon
        centroid_x = sum(x for x, _ in vertices) / len(vertices)
        centroid_y = sum(y for _, y in vertices) / len(vertices)

        # Display the region name at the centroid
        plt.text(centroid_x, centroid_y, region_name, ha='center', va='center', fontsize=8, color='black')

    yaxis = (clay*0.866025)
    xaxis = ((100-sand)-clay*0.5)
    # Plot a marker at the intersection point using simple method
    spoint = plt.plot(xaxis,yaxis, marker='o', color='red')


    #Funtion for determining the region of point
    def is_point_in_polygon(point, polygon):
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            x_intersection = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= x_intersection:
                                inside = not inside
            p1x, p1y = p2x, p2y

        return inside


    user_point = (xaxis, yaxis)

    # Determining the region for the user's point
    for region_name, vertices in regions.items():
        if is_point_in_polygon(user_point, vertices):
            region_name = region_name
            break

 

    # Ploting the graph
    tax.ticks(axis='blr', multiple=10, linewidth=2, offset=0.025, clockwise=True)
    tax.get_axes().axis('off')
    tax.clear_matplotlib_ticks()
    plt.tick_params(left = False, bottom = False)

    ternary.plt.plot()
    figure.savefig('static/css/my_plot.png')
    return render_template('index.html', sand=sand, clay= clay, silt=silt, soil_name = region_name, plot_url ='static/css/my_plot.png')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
