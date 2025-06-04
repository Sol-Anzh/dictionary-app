from customtkinter import *
import requests

app = CTk()
app.geometry("900x500")
app.title("Dictionary App")
set_appearance_mode("dark")

frame = CTkFrame(app, width=900, height=500)
frame.pack(expand=True, fill="both", padx=20, pady=20)

label = CTkLabel(frame, text="Simple Dictionary Application", font=("Helvetica", 18, "bold"), text_color="#18f181")
label.place(relx=0.5, rely=0.1, anchor="center")


entry = CTkEntry(frame, placeholder_text="Enter a word", height=50, width=500, font=("Helvetica", 14))
entry.place(relx=0.5, rely=0.3, anchor="center")

result_box = CTkTextbox(frame, width=600, height=250, font=("Helvetica", 14), wrap="word")
result_box.place(relx=0.5, rely=0.65, anchor="center")
result_box.configure(state="disabled") 

def search_word():
    word = entry.get()
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            phonetic = data[0].get('phonetic', '')
            output = f"Word: {word}\nPhonetic: {phonetic}\n\n"

            for meaning in data[0]['meanings']:
                part_of_speech = meaning.get('partOfSpeech', 'N/A')
                output += f"Part of Speech: {part_of_speech}\n"

                for idx, definition_obj in enumerate(meaning['definitions']):
                    definition = definition_obj.get('definition', 'No definition provided.')
                    output += f"  {idx + 1}. {definition}\n"

                    synonyms = definition_obj.get('synonyms', [])
                    if synonyms:
                        synonyms_text = ', '.join(synonyms)
                        output += f"     Synonyms: {synonyms_text}\n"

                output += "\n"

            result_box.configure(state="normal")   
            result_box.delete("1.0", "end")        
            result_box.insert("1.0", output)       
            result_box.configure(state="disabled") 

        except (KeyError, IndexError):
            result_box.configure(text="Definition not available.")
    else:
        result_box.configure(text="Word not found or not in dictionary.")



btn = CTkButton(frame, text="Search", height=50, width=150, font=("Helvetica", 14, "bold"), text_color="#000000", hover_color="#65f0a8", fg_color= "#18f181", command=search_word)
btn.place(relx=0.7, rely=0.3, anchor="center")

frame.place(relx=0.5, rely=0.5, anchor="center")


app.mainloop()
