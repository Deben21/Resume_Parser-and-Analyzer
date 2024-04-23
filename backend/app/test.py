entities =[['Name', 'Michael Smith'],['Certification', 'Data Science'],['Degree', 'Data Analyst'], ['Location', 'Manchester'], ['Email Address', 'indeed.com/r/falicent/140749dace5dc26f'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['Companies worked at', 'Microsoft'], ['College Name', 'The University of Manchester'], ['Skills', 'problem solving (Less than 1 year), project lifecycle (Less than 1 year), project \nmanager (Less than 1 year), technical assistance. (Less than 1 year)']]    
if entities:
    # Save extracted data to Parse model instance
    print(entities)
    name = ""
    college_name = ""
    skills = ""
    companies = ""
    experience = ""
    location = ""
    certification = ""

    for entity in entities:
        if entity[0] == 'Name':
            name = entity[1]
        elif entity[0] == 'College Name':
            college_name = entity[1]
        elif entity[0] == 'Skills':
            skills = entity[1]
        elif entity[0] == 'Companies worked at':
            companies = entity[1]
        elif entity[0] == 'Years of experience':
            experience = entity[1]
        elif entity[0] == 'Degree' or entity[0] == 'Certification':
            certification = entity[1]

    print("Name:", name)
    print("College Name:", college_name)
    print("Skills:", skills)
    print("Years of experience:", experience)
    print("Companies worked at:", companies)
    print("Degree/Certification:", certification)

