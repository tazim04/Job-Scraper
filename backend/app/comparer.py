# import re
# from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk import pos_tag
# from pypdf import PdfReader
# from transformers import AutoTokenizer, AutoModel
# from sklearn.metrics.pairwise import cosine_similarity
# import torch
# import os
# import nltk

# # Downlaod required NLTK resources
# # Add custom path if necessary (Docker)
# nltk.data.path.append('/usr/share/nltk_data')

# # # Automatically download required resources if not already present
# # nltk.download("punkt", download_dir='/usr/share/nltk_data')
# # nltk.download('punkt_tab')
# # nltk.download("stopwords", download_dir='/usr/share/nltk_data')
# # nltk.download("averaged_perceptron_tagger", download_dir='/usr/share/nltk_data')
# # nltk.download('averaged_perceptron_tagger_eng')


# class Comparer:
#     def __init__(self):
#         # Load BERT tokenizer and model
#         model_name = "bert-base-uncased"
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModel.from_pretrained(model_name).eval()

#         # Use GPU if available
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         self.model.to(self.device)

#     # Preprocess text: Lowercase, remove special characters, tokenize, and filter stopwords
#     def preprocess_text(self, text):
#         text = text.lower()
#         text = re.sub('[^a-zA-Z]', ' ', text)
#         sentences = sent_tokenize(text)
#         stop_words = set(stopwords.words("english")) # Load english stop words
#         processed_text  = []
        
#         for sent in sentences:
#             words = word_tokenize(sent)
#             words = [word for word in words if word not in stop_words]
#             tagged_words = pos_tag(words)
#             filtered_words = [word for word, tag in tagged_words if tag not in ['DT', 'IN', 'TO', 'PRP', 'WP']]
#             processed_text .append(" ".join(filtered_words))
        
#         return " ".join(processed_text )

#     # Extract resume text from pdf
#     def extract_text_from_pdf(self, file_path):
#         reader = PdfReader(file_path)
#         return "".join(page.extract_text() for page in reader.pages)

#     # Generate BERT embeddings
#     def get_bert_embedding(self, text):
#         inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512).to(self.device) # Tokenize text for BERT
#         with torch.no_grad(): # Inference mode
#             outputs = self.model(**inputs)
#         embedding = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()  # Use the [CLS] token representation
#         return embedding

#     # Calculate cosine similarity between two embeddings
#     def calculate_similarity(self, resume_text, job_desc_text):
#         resume_embedding = self.get_bert_embedding(self.preprocess_text(resume_text))
#         job_desc_embedding = self.get_bert_embedding(self.preprocess_text(job_desc_text))
#         similarity = cosine_similarity([resume_embedding], [job_desc_embedding])[0][0]
#         return similarity

#     # Batch process resumes against a single job description
#     def match_resumes_to_job(self, job_desc_text, resume_file):
#         # Extract and preprocess the resume text
#         resume_text = self.extract_text_from_pdf(resume_file)
#         processed_resume = self.preprocess_text(resume_text)
        
#         # print(resume_text)
        
#         # Preprocess the job description
#         processed_job_desc = self.preprocess_text(job_desc_text)
        
#         print("Preprocessed Resume:", processed_resume)
#         print("Preprocessed Job Description:", processed_job_desc)
        
#         # Generate embeddings
#         resume_embedding = self.get_bert_embedding(processed_resume)
#         job_desc_embedding = self.get_bert_embedding(processed_job_desc)
        
#         # Debugging: Analyze embeddings
#         print("Resume Embedding Sample:", resume_embedding[:5])  # Print first 5 values
#         print("Job Description Embedding Sample:", job_desc_embedding[:5])  # Print first 5 values
        
#         # Calculate similarity
#         similarity = cosine_similarity([resume_embedding], [job_desc_embedding])[0][0]
#         print("Similarity Score:", similarity)
        
#         return {"file": resume_file, "similarity": similarity}



#     # Test the workflow
#     def test(self):
#         # Example job description
#         job_description = """
# Job Summary:
# We are seeking dedicated and disciplined individuals to join the military as Infantry Soldiers. This role involves protecting national security, performing tactical operations, and contributing to the success of missions in diverse environments. Infantry Soldiers operate as part of a team, often in challenging and high-pressure situations.

# Key Responsibilities:

# Conduct combat and reconnaissance operations on land, in various terrains, and under diverse weather conditions.
# Operate and maintain a variety of weapons, vehicles, and equipment used in tactical missions.
# Patrol and secure assigned areas to ensure safety and prevent unauthorized access.
# Engage in defensive and offensive actions during military operations.
# Coordinate with team members to execute missions effectively and safely.
# Participate in physical training to maintain peak fitness levels required for the role.
# Assist in humanitarian missions, disaster response, and peacekeeping operations.
# Perform first aid and provide emergency medical care to injured team members or civilians.
# Qualifications:

# High school diploma or equivalent; some roles may require additional education or certifications.
# Must meet physical and medical requirements for enlistment.
# Strong sense of discipline, teamwork, and adaptability.
# Willingness to follow orders and maintain strict adherence to protocols.
# Ability to remain calm and perform effectively under stress.
# U.S. citizen or permanent resident (for most positions).
# Preferred Skills:

# Proficiency in weapons handling and marksmanship.
# Knowledge of basic navigation and map-reading techniques.
# Experience with teamwork in high-pressure environments.
# Strong problem-solving and critical-thinking abilities.
# First aid or emergency medical training is an advantage.
# Working Conditions:

# Rigorous training and physical demands, including long hours and potentially hazardous conditions.
# Deployment to various locations, including overseas assignments, with extended periods away from home.
# Exposure to extreme weather, challenging terrains, and potential combat zones.
# Close collaboration with diverse teams in dynamic and unpredictable environments.

#         """

#         # Example resume in PDF files
#         base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Navigate to the project root
#         resume_path = os.path.join(base_dir, "Resume - Tazim Khan.pdf")

#         # Match resumes to the job description
#         result = self.match_resumes_to_job(job_description, resume_path)

#         # Return results instead of printing
#         return {
#             "file": result["file"],
#             "similarity": f"{result['similarity']:.2f}",
#         }
            
