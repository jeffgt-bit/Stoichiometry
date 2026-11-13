from bakery import assert_equal
from dataclasses import dataclass, field
from drafter import *
import re
set_website_title("Stoichiometry_Code")
set_site_information(
    author="Jeffrey Fu",
    description="Simple stoichiometry with balenced equations.",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)

""" Molar masses of all the elements on the periodic table.
     Source: https://pubchem.ncbi.nlm.nih.gov/ptable/atomic-mass/"""
molar_masses = {
    "H": 1.0080,
    "He": 4.00260,
    "Li": 7.0,
    "Be": 9.012183,
    "B": 10.81,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.99840316,
    "Ne": 20.180,
    "Na": 22.9897693,
    "Mg": 24.305,
    "Al": 26.981538,
    "Si": 28.085,
    "P": 30.97376200,
    "S": 32.07,
    "Cl": 35.45,
    "Ar": 39.9,
    "K": 39.0983,
    "Ca": 40.08,
    "Sc": 44.95591,
    "Ti": 47.867,
    "V": 50.9415,
    "Cr": 51.996,
    "Mn": 54.93804,
    "Fe": 55.84,
    "Co": 58.93319,
    "Ni": 58.693,
    "Cu": 63.55,
    "Zn": 65.4,
    "Ga": 69.723,
    "Ge": 72.63,
    "As": 74.92159,
    "Se": 78.97,
    "Br": 79.90,
    "Kr": 83.80,
    "Rb": 85.468,
    "Sr": 87.62,
    "Y": 88.90584,
    "Zr": 91.22,
    "Nb": 92.90637,
    "Mo": 95.95,
    "Tc": 96.90636,
    "Ru": 101.1,
    "Rh": 102.9055,
    "Pd": 106.42,
    "Ag": 107.868,
    "Cd": 112.41,
    "In": 114.818,
    "Sn": 118.71,
    "Sb": 121.760,
    "Te": 127.6,
    "I": 126.9045,
    "Xe": 131.29,
    "Cs": 132.9054520,
    "Ba": 137.33,
    "La": 138.9055,
    "Ce": 140.116,
    "Pr": 140.90766,
    "Nd": 144.24,
    "Pm": 144.91276,
    "Sm": 150.4,
    "Eu": 151.964,
    "Gd": 157.25,
    "Tb": 158.92535,
    "Dy": 162.500,
    "Ho": 164.93033,
    "Er": 167.26,
    "Tm": 168.93422,
    "Yb": 173.05,
    "Lu": 174.9667,
    "Hf": 178.49,
    "Ta": 180.9479,
    "W": 183.84,
    "Re": 186.207,
    "Os": 190.2,
    "Ir": 192.22,
    "Pt": 195.08,
    "Au": 196.96657,
    "Hg": 200.59,
    "Tl": 204.383,
    "Pb": 207.0,
    "Bi": 208.98040,
    "Po": 208.98243,
    "At": 209.98715,
    "Rn": 222.01758,
    "Fr": 223.01973,
    "Ra": 226.02541,
    "Ac": 227.02775,
    "Th": 232.038,
    "Pa": 231.03588,
    "U": 238.0289,
    "Np": 237.048172,
    "Pu": 244.06420,
    "Am": 243.061380,
    "Cm": 247.07035,
    "Bk": 247.07031,
    "Cf": 251.07959,
    "Es": 252.0830,
    "Fm": 257.09511,
    "Md": 258.09843,
    "No": 259.10100,
    "Lr": 266.120,
    "Rf": 267.122,
    "Db": 268.126,
    "Sg": 269.128,
    "Bh": 270.133,
    "Hs": 269.1336,
    "Mt": 277.154,
    "Ds": 282.166,
    "Rg": 282.169,
    "Cn": 286.179,
    "Nh": 286.182,
    "Fl": 290.192,
    "Mc": 290.196,
    "Lv": 293.205,
    "Ts": 294.211,
    "Og": 295.216
}


@dataclass
class Chemical:
    """Dataclass of the a reactant or product of the reaction.
       Attributes:
        reactant:Abbreviated reactant formula.
        product:Abbreviated product formula.
        starting_mass: Starting mass of the chemical.
        molar_mass:Molar mass of the chemical.
        moles:Amount of moles of the chemical.
        coefficient: Chemical coefficient of the chemical in terms of the reaction."""
    reactant:str
    product:str
    starting_mass:float
    molar_mass:float
    moles:float
    coefficient:int=1
    
@dataclass
class State:
    """ Current state of the Stoichiometry_Code/ 
        (Field allows every new State to start with page_show page_show.)
        Attributes:
         reaction: The entire chemical reaction.
         reactants: All the reactants of the chemical reaction.
         products: All the reactants of the chemical reaction.
         total_moles_product: Total moles of the products in the chemical reaction.
         verify: Verifies if the user is ok with proceeding.
         limiting_reactant: Limiting reactant of the provided reactants.
         limiting_moles: The amount of moles that the limitng reactant has."""
    reaction:str = ""
    reactants:list[Chemical] = field(default_factory=list)
    products:list[Chemical]= field(default_factory=list)
    total_moles_product:float = 0.0
    verify:bool = False
    limiting_reactant: str=""
    limiting_moles: float=0.0


@route
def index(state:State)->Page:
    """The starting page where the user inputs the reactants from their balenced reaction."""
    return Page(state,[
            "Insert Balanced Reactants Abbreviated With Correct Capitalization: Example: 1C2H4 and 3O2",
             TextBox("reactant"),
             Button("Enter Reactant","reactant"),   
             Button("Next Page","reactant_amount")])

@route
def reactant (state:State,reactant:str)-> Page:
    """Updates the page to show the reactants that the user has inputted.
       Allows the user to input more reactants or to proceed."""
    coefficient,formula= split_coefficient(reactant)
    if reactant.strip() != "":
       new_chemical=Chemical(formula,"",0.0,0.0,0.0,coefficient)
       state.reactants.append(new_chemical)
    
    return Page(state,
             ["Insert Balanced Reactants Abbreviated With Correct Capitalization: Example: 1C2H4 and 3O2" + "\n",
             *[chemical.reactant.strip() + "\n" for chemical in state.reactants],
             TextBox("reactant") ,
             Button("Enter Reactant","reactant"),   
             Button("Next Page","reactant_amount")])
@route  
def reactant_amount (state:State)-> Page:
    """ User inputs the amount of reactants in grams.
    (Uses f-string)"""
    page_show=["Insert Reactant Amounts in Grams:"]
    for index, chemical in enumerate (state.reactants):
        page_show.append(Row([chemical.reactant,
        TextBox(f"mass_{index}")]))
    page_show.append(Button("Save Masses", "mass_saver"))
    return Page(state,page_show)
@route
def mass_saver (state:State, **kwargs)->Page:
    """Tell the user that their masses are saved."""
    for index, chemical in enumerate(state.reactants):
        chemical.starting_mass=float(kwargs.get(f"mass_{index}",0))
    return Page(state,[
        "Masses are saved!!!",
        Button("Next Page", "product_page")])

@route
def product_page (state:State)-> Page:
    """Allows the user to input the products of the chemical reaction."""
    return Page(state,[
            "Insert Balanced Products Abbreviated With Correct Capitalization: Example: 2CO2 and 2H2O",
             TextBox("product"),
             Button("Enter Product","product"),   
             Button("Next Page","verify")])
    
@route
def product(state:State,product:str)->Page:
    """Allows the user input more products and saves them in State."""
    coefficient, formula = split_coefficient(product)
    if product.strip() != "":
       new_chemical=Chemical("",formula,0.0,0.0,0.0,coefficient)
       state.products.append(new_chemical)
    
    return Page(state,
             ["Insert Balanced Products Abbreviated With Correct Capitalization: Example: 2CO2 and 2H2O" + "\n",
             *[chemical.product.strip() + "\n" for chemical in state.products],
             TextBox("product") ,
             Button("Enter Product","product"),   
             Button("Next Page","verify")])

def reaction_builder (state:State):
    """Builds the  full reaction of that includes the products and reactants."""
    reactants = " + " .join(str(chemical.coefficient) + chemical.reactant for chemical in state.reactants)
    products= " + ".join( str(chemical.coefficient) + chemical.product for chemical in state.products)
    state.reaction= reactants + "->" + products
    return state.reaction


@route
def verify(state: State) -> Page:
    """Displays the full chemical reaction to the user and the amount of reactants in grams"""
    reactant_list = []
    product_list=[]
    reaction_builder(state)
    for chemical in state.reactants:
        reactant_list.append(
            chemical.reactant + " - " +
            str(chemical.starting_mass) + " g" )

    for chemical in state.products:
        product_list.append(str(chemical.coefficient) + chemical.product)
    
    return Page(state, [
        "Verify Your Reaction",
        "Balanced Equation:" + "\n",
        state.reaction + "\n",
        "Reactants and Starting Masses:" + "\n",
        *reactant_list,
        "Products:",
        *product_list,
        Button("Confirm", "product_mole"),
        Button("Go Back", "edit_reactants")
        ])
@route
def edit_reactants(state:State)->Page:
    "Allows the User to Edit thier reactants."
    return Page(state, [ "Edit your Reactants:",
                       *[chemical.reactant for chemical in state.reactants],
                       TextBox("reactant"),
                       Button("Enter Reactant", "reactant"),
                       Button("Continue","reactant_amount")])

def get_molar_mass(formula):
    """Gets the molar masses of the product/reactant of the chemical formula."""
    total=0
    elements= re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    if not elements or "".join(element+amount for element, amount in elements) != formula:
        raise ValueError ("Invalid Chemical Formula.")
    for element, amount in elements:
        if amount=="":
            amount=1
        else:
            amount=int(amount)
        if element not in molar_masses:
            raise ValueError("Unkown element: "+ element)
        total+=molar_masses[element] * amount
    return total
assert_equal(round(get_molar_mass("H2O"),3), 18.015)
assert_equal(round(get_molar_mass("O2"),3), 31.998)

def parse_formula(formula: str):
    """Finds the the number specififc atoms of a chemical"""
    elements = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    parsed = []
    for element, subscript in elements:
        if subscript == "":
            subscript = 1
        else:
            subscript = int(subscript)
        parsed.append((element, subscript))
    return parsed
assert_equal(parse_formula("H2O"), [("H",2),("O",1)])
def limiting_reactant (state:State):
    """Defines the limiting reactant by dividing the moles by the coefficient."""
    smallest= float("inf")
    limiting_chemical=None
    
    for chemical in state.reactants:
        ratio=chemical.moles/chemical.coefficient
        if ratio < smallest:
            smallest=ratio
            limiting_chemical=chemical
    if limiting_chemical is None:
        return None
    state.limiting_reactant = limiting_chemical.reactant
    state.limiting_moles = smallest
    return limiting_chemical
   
def reactant_mole(state:State):
    """Finds the moles of the reactant after the coefficient is seperated from the formula."""
    reactant_results=[]
    for chemical in state.reactants:
        chemical.molar_mass=get_molar_mass(chemical.reactant)
        chemical.moles=(chemical.starting_mass / chemical.molar_mass)
        reactant_results.append(chemical.reactant+ ": " + str(round(chemical.moles,3))+ " moles")
    return reactant_results
def split_coefficient(entry):
    """Parses through a chemical and seperates the coefficient from its formula."""
    match=re.fullmatch(r"(\d*)([A-Z][A-Za-z0-9]*)", entry.strip())
    if not match:
        raise ValueError("Invalid Formula")
    coefficient= int(match.group(1)) if match.group(1) else 1
    if coefficient<=0:
        raise ValueError("Error:Coefficient must be greater than zero!")
    formula=match.group(2)
    return coefficient, formula

assert_equal(split_coefficient("2H2O"),(2,"H2O"))
assert_equal(split_coefficient("O2"),(1,"O2"))

@route
def product_mole(state:State)->Page:
    """Displays the moles of each product and allows the user to return to index for a new reaction."""
    reactant_mole(state)
    limiting=limiting_reactant(state)
    if limiting is None:
        return Page(state, ["Error: Limiting reactant not found."])
    resulting_product = []
    for chemical in state.products:
        chemical.moles =state.limiting_moles*chemical.coefficient
        resulting_product.append (chemical.product+ ": " +str(round(chemical.moles,3))+" mole")
    return Page(state,["Limiting Reactant:" + limiting.reactant,"Moles of Products:", *resulting_product, Button("New Equation ", "new_equation"
                                                                                                                 )])
@route
def new_equation(state:State)->Page:
    "Resets all of State for new formula."
    state.reactants=[]
    state.products=[]
    state.reaction=""
    state.total_moles_product = 0.0
    state.limiting_reactant= ""
    state.limiting_moles= 0.0
    return index(state)
    
start_server(State())


