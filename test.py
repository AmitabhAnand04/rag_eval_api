from services.cosmos_service import get_item, get_item_for_evaluation, get_score_item, insert_items, update_item, update_score_list
# from utils.refactor import transform_to_df, extract_questions_to_df, transform_data

# input_list = [
#     {
#         "user_input": "Wht is cerebrovasculr diseas?",
#         "reference_contexts": [
#             "Heart\tDisease\tIntroduction: Heart disease describes a range of conditions that affect the heart. Diseases under the umbrella term heart disease include: • Cardiovascular disease. • Heart arrhythmia. • Congenital heart disease.  • Cardiomyopathy. • Heart disease caused by heart infections. • Heart valve disease.  Symptoms:  Heart disease symptoms vary depending on which type of heart diseases you have.  Cardiovascular disease: Cardiovascular disease can result in narrowed or blocked blood vessels that restrict blood circulation to the heart, brain, or other parts of the body. Symptoms of cardiovascular disease include: • Coronary artery disease - a disease affecting the major blood vessels that supply the heart with blood, oxygen, and nutrients.  • Cerebrovascular disease - a disease affecting the blood vessels supplying the brain. • Peripheral artery disease - a disease affecting the blood vessels supplying the arms and legs. • Rheumatic heart disease - damage to the heart muscle and heart valves resulting from rheumatic fever, which is caused by an infection from streptococcal bacteria. • Congenital heart disease - heart defects that are observed at birth."
#         ],
#         "reference": "Cerebrovascular disease is a condition affecting the blood vessels supplying the brain.",
#         "synthesizer_name": "single_hop_specifc_query_synthesizer"
#     },
#     {
#         "user_input": "What is a pulmonary embolism?",
#         "reference_contexts": [
#             "• Pulmonary embolism - blood clots that come from leg veins, which can dislodge and move to the heart and lungs. Heart attacks and strokes are dangerous medical conditions that are mainly caused by a blockage that prevents blood from flowing to the heart or brain. The most common reason for this blockage is a build-up of fatty deposits on the inner walls of the blood vessels that supply the heart or brain. Strokes can also be caused by bleeding from a blood vessel in the brain or from blood clots.    What Are the Risk Factors for Cardiovascular Disease? The most important behavioral risk factors leading to heart disease and strokes are: • An unhealthy diet. • Physical inactivity. • Smoking. • Alcohol consumption. • High blood pressure. • Diabetes. • High blood cholesterol and fat levels. • Obesity.   What Are Common Symptoms of Cardiovascular Diseases? Often, there are no symptoms or warning signs that indicate that a person is suffering from a cardiovascular disease. A heart attack or stroke may be the first warning sign or indicator of the disease.   Symptoms of a Heart Attack Include: • Pain or discomfort in the center of the chest. • Pain or discomfort in the arms, the left shoulder, elbows, jaw, or back."
#         ],
#         "reference": "A pulmonary embolism is a condition where blood clots come from leg veins, which can dislodge and move to the heart and lungs.",
#         "synthesizer_name": "single_hop_specifc_query_synthesizer"
#     }
# ]

# output = transform_data(input_list)
# print(output)
# print("------------------------------------------------")
# print(insert_items(output))
# print(get_item(fileID="2eed3f93-9822-4715-9b37-ade11e713dc3"))
# question_responses = {
#     "21c08461-192a-45d4-b83c-e894bd7b34d9": "Response for cerebrovascular disease",
#     "615429a9-3e7f-4f19-92af-2410bd4b784c": "Response for pulmonary embolism"
#     }
# print(update_item("2eed3f93-9822-4715-9b37-ade11e713dc3", question_responses))

# print(get_item_for_evaluation("2eed3f93-9822-4715-9b37-ade11e713dc3"))
# data = [
#     {
#         "testset": [
#             {
#                 "questionID": "13f34770-0175-40f7-acda-18c63820af39",
#                 "user_input": "What heart disease mean and what types there is?",
#                 "reference_contexts": [
#                     "Heart\tDisease\tIntroduction: Heart disease describes a range of conditions that affect the heart. Diseases under the umbrella term heart disease include: • Cardiovascular disease. • Heart arrhythmia. • Congenital heart disease.  • Cardiomyopathy. • Heart disease caused by heart infections. • Heart valve disease.  Symptoms:  Heart disease symptoms vary depending on which type of heart diseases you have.  Cardiovascular disease: Cardiovascular disease can result in narrowed or blocked blood vessels that restrict blood circulation to the heart, brain, or other parts of the body. Symptoms of cardiovascular disease include: • Coronary artery disease - a disease affecting the major blood vessels that supply the heart with blood, oxygen, and nutrients.  • Cerebrovascular disease - a disease affecting the blood vessels supplying the brain. • Peripheral artery disease - a disease affecting the blood vessels supplying the arms and legs. • Rheumatic heart disease - damage to the heart muscle and heart valves resulting from rheumatic fever, which is caused by an infection from streptococcal bacteria. • Congenital heart disease - heart defects that are observed at birth."
#                 ],
#                 "reference": "Heart disease describes a range of conditions that affect the heart, including cardiovascular disease, heart arrhythmia, congenital heart disease, cardiomyopathy, heart disease caused by heart infections, and heart valve disease.",
#                 "synthesizer_name": "single_hop_specifc_query_synthesizer",
#                 "response": "Response for cerebrovascular disease"
#             },
#             {
#                 "questionID": "62d22251-d344-4014-b830-3b1c68d804a7",
#                 "user_input": "What are the types of heart infections and their symptoms, and how do they relate to other heart diseases?",
#                 "reference_contexts": [
#                     "<1-hop>\n\nHeart\tDisease\tIntroduction: Heart disease describes a range of conditions that affect the heart. Diseases under the umbrella term heart disease include: • Cardiovascular disease. • Heart arrhythmia. • Congenital heart disease.  • Cardiomyopathy. • Heart disease caused by heart infections. • Heart valve disease.  Symptoms:  Heart disease symptoms vary depending on which type of heart diseases you have.  Cardiovascular disease: Cardiovascular disease can result in narrowed or blocked blood vessels that restrict blood circulation to the heart, brain, or other parts of the body. Symptoms of cardiovascular disease include: • Coronary artery disease - a disease affecting the major blood vessels that supply the heart with blood, oxygen, and nutrients.  • Cerebrovascular disease - a disease affecting the blood vessels supplying the brain. • Peripheral artery disease - a disease affecting the blood vessels supplying the arms and legs. • Rheumatic heart disease - damage to the heart muscle and heart valves resulting from rheumatic fever, which is caused by an infection from streptococcal bacteria. • Congenital heart disease - heart defects that are observed at birth.",
#                     "<2-hop>\n\nCardiomyopathy: Cardiomyopathy is a disease that affects the heart muscle. In early stages of cardiomyopathy, the patient may not have any symptoms, but as the condition worsens, symptoms may include:  • Shortness of breath with exertion or at rest. • Swelling in the legs, ankles, and feet. • Bloating of the abdomen due to fluid buildup. • Fatigue. • Irregular heartbeats that feel rapid, pounding, or fluttering. • Dizziness, lightheadedness, and fainting.  Heart Disease Caused by Heart Infections: There are three types of heart infections: • Pericarditis (inflammation of the pericardium, which is the fibrous sac surrounding the heart). • Myocarditis (inflammation of the myocardium, which is the thick middle layer of the heart muscle). • Endocarditis (inflammation of the endocardium, which is the inner lining of your heart chambers and heart valves). Heart infection symptoms can include: • Fever. • Shortness of breath. • Fatigue. • Swelling in the legs or abdomen. • Heart rhythm irregularities. • Dry or persistent cough. • Skin rashes or unusual spots."
#                 ],
#                 "reference": "Heart infections can be categorized into three types: pericarditis, myocarditis, and endocarditis. Pericarditis is the inflammation of the pericardium, myocarditis is the inflammation of the myocardium, and endocarditis is the inflammation of the endocardium. Symptoms of heart infections include fever, shortness of breath, fatigue, swelling in the legs or abdomen, heart rhythm irregularities, dry or persistent cough, and skin rashes or unusual spots. These infections can lead to heart disease, as they may cause damage to the heart muscle and heart valves, contributing to conditions such as rheumatic heart disease, which is a result of an infection from streptococcal bacteria. Additionally, symptoms like shortness of breath and swelling are also common in other heart conditions such as cardiomyopathy.",
#                 "synthesizer_name": "multi_hop_specific_query_synthesizer",
#                 "response": "Response for pulmonary embolism"
#             }
#         ]
#     }
# ]
# # print(extract_questions_to_df(data))
# print(extract(data))

# Example usage
# fileID = "d3dc255e-c860-41d0-9bea-1516c54658ca"
# questionID = "13f34770-0175-40f7-acda-18c63820af39"
# scoreList = [
#     {"metric":"score1", "score": 34},
#     {"metric":"score2", "score": 3},
#     {"metric":"score3", "score": 2124},
#     {"metric":"score4", "score": 2365},
# ]
# update_score_list(fileID, questionID, scoreList)
# fileID = "2eed3f93-9822-4715-9b37-ade11e713dc3"
# print(get_score_item(fileID=fileID))
