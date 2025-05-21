from flask import Flask, render_template, request
import pickle
import numpy as np
import os
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf

app = Flask(__name__)

# Load your model (using pickle for simplicity or you can use the keras model load)
# If you're using pickle:
model = pickle.load(open('model.pkl', 'rb'))


waste_info = {
    "Battery": {
        "info": "Batteries contain hazardous materials. Recycle them at designated drop-off locations. Batteries contain hazardous chemicals like lead, cadmium, and mercury, which can contaminate soil and water if disposed of improperly. Single-use alkaline batteries (AA, AAA, 9V, etc.) can sometimes be thrown in regular trash, but it is best to check your local recycling guidelines. Rechargeable batteries (lithium-ion, nickel-metal hydride, etc.) must be recycled at designated drop-off locations, such as electronics stores or battery recycling centers. Car batteries (lead-acid, lithium-ion, etc.) should never be thrown in the trash; instead, they must be returned to auto shops or hazardous waste facilities. To safely store and transport old batteries, place them in a fireproof container or cover the terminals with tape to prevent short-circuiting.",
        "points":['Disposing of batteries responsibly in India is crucial to prevent environmental harm. Here are some effective methods:',
            '1. Segregation : Separate used batteries from regular trash to avoid contamination.',
            '2. Collection Centers : Many cities have designated collection centers for battery disposal.',
            '3. Recycling Facilities : Batteries can be sent to specialized recycling facilities to recover valuable materials like lead, lithium, and nickel.',
            '4. Retailer Programs : Some retailers accept used batteries for proper disposal.',
            '5. Municipal Services : Local municipalities often have guidelines or services for battery disposal.',
            '6. Avoid Landfills : Never throw batteries in regular trash bins, as they can leak hazardous chemicals.'],
        "video": "https://www.youtube.com/embed/D7td95ySam8",
        
    },
    "Cardboard": {
        "info": "Flatten and place cardboard in recycling bins. Avoid wet or greasy cardboard. Cardboard is highly recyclable, but proper preparation is necessary for effective processing. Flatten all cardboard boxes before placing them in curbside recycling to save space. Remove any plastic tape, labels, or stickers before recycling. Wet or greasy cardboard, such as food-stained pizza boxes, should not be placed in regular recycling bins. Instead, compost them if possible. Some types of cardboard, like waxed or laminated cardboard (juice cartons, frozen food boxes), may not be recyclable in all areas. Always check with your local waste management service to confirm the best disposal method. ",
        "points":['Here are some ways to dispose of cardboard responsibly :',
            '1. Recycling : Take cardboard to nearby recycling centers or give it to local scrap dealers (kabadiwalas). They will ensure it gets processed for reuse. Many urban areas have waste collection programs that include cardboard recycling.',
            '2. Reuse :Use cardboard for storage, moving, or as protective packaging. Get creative by repurposing it into organizers, toys, or craft projects.',
            "3. Composting : Non-coated cardboard (no plastic or wax coating) can be shredded and added to a compost pile. It's a great source of carbon and balances out food waste.",
            '4. Community Initiatives : Some NGOs and community-led programs accept cardboard donations for recycling or reuse. Schools or art organizations may also accept cardboard for projects.',
            '5. Packaging Companies : Some courier and packaging companies take back cardboard boxes to reuse or recycle.'],
        "video": "https://www.youtube.com/embed/FB3cM-CgPGQ",
        
    },
    "Paper": {
        "info": "Recycle clean paper products. Avoid wax-coated paper. Paper products are widely recyclable, but not all paper waste is suitable for recycling. Clean paper, newspapers, magazines, and office paper should be placed in the paper recycling bin. Shredded paper may require special handling; check with your local recycler on whether it needs to be placed in a separate bag. Certain types of paper, such as wax-coated, laminated, or greasy paper (e.g., pizza boxes, napkins, and tissues), cannot be recycled and should be composted instead. To ensure efficient recycling, keep paper dry and separate from food waste. ",
        "points":[ 'Here are some responsible ways to dispose of paper :',
            '1. Recycling : Hand over old newspapers, notebooks, or other paper waste to local scrap dealers (kabadiwalas) or recycling centers. Many cities have organized waste collection services that include paper recycling.',
            '2. Reuse : Use one-sided paper for rough work, notes, or craft activities.Create envelopes, bookmarks, or gift wraps using waste paper.',
            '3. Composting : Shred non-glossy paper (free from plastic or wax coatings) and add it to your compost bin as a carbon-rich component.',
            '4. Community Donations : Donate usable paper (like blank pages from old notebooks) to schools or NGOs. Organizations focusing on upcycling may use waste paper for creative projects.',
            '5. Upcycling : Turn waste paper into DIY products like papier-mâché crafts, storage boxes, or decorations.',
            '6. Avoid Burning : Avoid burning paper, as it releases harmful pollutants into the air.',
            'By adopting these methods, you can help reduce waste and support sustainability.'
        ],
        "video": "https://www.youtube.com/embed/jAqVxsEgWIM",
    
    },
    "Food": {
        "info": "Compost organic waste or use food scrap recycling services. Food waste can be managed effectively through composting, donation, and responsible disposal. Fruit and vegetable scraps, eggshells, coffee grounds, and plant-based leftovers should be composted to create nutrient-rich soil. Many cities offer food scrap collection services, which allow organic waste to be processed into compost or biogas. For uneaten or surplus food, consider donating to food banks or shelters instead of throwing it away. Items like meat, dairy, and oily foods should not be composted in home composting bins, as they attract pests and require commercial composting facilities. ",
        "points":['Here are some ways to dispose of food responsibly :',
            '1. Composting : Food waste can be turned into nutrient-rich compost for gardens or plants. You can use home composting kits or community composting facilities.',
            '2. Biogas Production : Set up or contribute to biogas plants where food waste is converted into biogas for cooking or energy.',
            '3. Animal Feed : Suitable food waste can be provided to farmers or animal shelters to feed livestock or stray animals.',
            '4. Donations : Excess edible food can be donated to NGOs, food banks, or community kitchens to help those in need.',
            '5. Vermicomposting : Use food scraps to create vermicompost with earthworms, which produces excellent fertilizer for plants.',
            '6. Waste Segregation : Always segregate food waste from other types of garbage to make it easier for waste pickers or municipal workers to process it properly.',
            'These methods not only reduce waste but also promote sustainable practices.'],
        "video": "https://www.youtube.com/embed/ishA6kry8nc",
        
    },
    "Metal": {
        "info": "Recycle metal cans and scrap metal at designated facilities. Metals are highly recyclable and can be repurposed into new products with minimal environmental impact. Aluminum cans (soda, beer, food cans) should be rinsed and placed in curbside recycling. Scrap metal, including old appliances, pipes, and car parts, should be taken to a metal recycling center. Small metal items, such as bottle caps and aluminum foil, can also be collected and recycled together. For electronic waste (e-waste) containing metal components, take them to an e-waste collection center rather than throwing them in the trash. Avoid recycling painted, coated, or contaminated metals, as these require special treatment. ",
        "points":['Here are some ways to responsibly dispose of metal :',
            '1. Recycling : Hand over metal waste to scrap dealers or recycling centers. They can process it for reuse in manufacturing new products.',
            '2. Upcycling : Repurpose metal items for home or industrial use, such as turning old cans into planters or decorative items.',
            '3. E-Waste Recycling : For metals found in electronic waste, such as copper or aluminum, use certified e-waste recycling services.',
            '4. Donations : Donate usable metal items like utensils or tools to organizations or individuals who may need them.',
            '5. Municipal Collection Services : Check if your local municipality has specialized services for collecting and recycling metal waste.',
            '6. Avoid Landfills : Metal should never be thrown in regular trash or landfills, as it can harm the environment and waste valuable resources.'],
        "video": "https://www.youtube.com/embed/d38cH4DyUxg",
       
    },
    "Plastic": {
        "info": "Check plastic codes and recycle accordingly. Avoid single-use plastics. Plastics are among the most common waste materials, but not all plastics are recyclable. The recycling number (♳ to ♹) on plastic containers helps determine whether an item can be recycled. Rigid plastics, such as water bottles and food containers, should be rinsed and placed in your curbside recycling bin. Plastic bags and film wraps should not be placed in regular recycling bins, as they can jam machinery—instead, return them to collection bins at grocery stores. Certain plastics, such as Styrofoam (polystyrene), PVC, and plastic-coated materials, are difficult to recycle and should be disposed of according to local waste management guidelines. ",
        "points":['Here are some ways to responsibly dispose of plastic :',
            '1. Recycling: Segregate plastic waste and hand it over to authorized recycling centers or local scrap dealers. They can process it for reuse in manufacturing.',
            '2. Reduce and reuse: Opt for reusing plastic bottles, containers, or bags as much as possible instead of discarding them.',
            '3. Avoid single-use plastics: Minimize the use of single-use items like plastic straws, cutlery, and bags by choosing sustainable alternatives.',
            '4. Upcycling: Get creative by turning plastic waste into useful or decorative items such as planters, storage boxes, or crafts.',
            '5. Community collection programs: Participate in local community initiatives or NGO programs that collect plastic waste for recycling or repurposing.',
            '6. EPR programs: Many brands in India follow Extended Producer Responsibility (EPR). Return plastic packaging to these companies for proper disposal or recycling.',
            '7. Municipal waste collection: Check with your local municipality for plastic waste collection services to ensure its proper handling and recycling.',
            'By following these methods, you can contribute to reducing plastic pollution and promoting sustainability'],
        "video": "https://www.youtube.com/embed/4JDGFNoY-rQ",
       
    }
}

# If you're using TensorFlow/Keras model, use the following line instead:
# model = tf.keras.models.load_model('your_model.h5')

# Set up the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to display the form
@app.route('/')
def home():
    return render_template('M1.html')

@app.route("/identify")
def identify():
    return render_template('identify.html')

# Route to handle the form submission and image processing
@app.route("/WasteIdentify", methods=['POST', 'GET'])
def WasteIdentify():
    if request.method == 'POST': 
    
        file = request.files['ImageInput']
        
        # If no file is selected
        if file.filename == '':
            return render_template('identify.html', pred=f'No selected file')

        # If the file is allowed, process it
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Open the image and preprocess it for your model
            image = Image.open(filepath)
            image = image.resize((256, 256))  # Resize to the model's expected input size
            image = np.array(image)  # Convert image to numpy array
            # If your model expects a batch dimension
            image = np.expand_dims(image, axis=0)
            # Get the model's prediction
            prediction = model.predict(image)
            # Assuming a classification model, get the class with the highest probability
            predicted_class = np.argmax(prediction, axis=1)
            # Define classes based on your model's outputs
            classes = ['Battery', 'Cardboard', 'Metal', 'Paper', 'Plastic', 'Food']
            # Return the result to the user
            info = waste_info.get(classes[predicted_class[0]], None)
            return render_template('identify.html', pred=f'Waste is: {classes[predicted_class[0]]}' , info=info)

            #return render_template('result.html', waste_type=waste_type, info=info)

            '''if classes[predicted_class[0]] == 'Battery':
                data='<h1>Battery</h1><br><p>lauren<p>'
            else :
                data='<h1>ELse</h1><br><p>lauren<p>'
            return render_template('identify.html', pred=data)'''

        return 'Invalid file format'

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/contactus")
def contactus():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=True)
