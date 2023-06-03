from tkinter import (
    Tk,
    ttk,
    Frame,
    Entry,
    Button,
    END,
    RIGHT,
    Label,
    Listbox,
    StringVar,
    filedialog,
    messagebox,
    Scrollbar,
)


class Gui(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # ---------- Title Frame ----------
        self.title_frame = Frame(self.parent, bg="#FFAE00")
        self.title_frame.pack(side="top", fill="both", expand=True)

        # Title Label
        self.title_label = Label(self.title_frame, text="Github Repository Recommender",
                                 fg="#FFFFFF", bg="#FFAE00", font=("Arial", 20))
        self.title_label.pack(side="top", fill="both", expand=True)

        # ---------- Button Frame ----------
        self.button_frame = Frame(self.parent, bg="#FFFFFF")
        self.button_frame.pack(side="top")

        # upload user data button
        self.upload_user_button = Button(
            self.button_frame, text="Upload User Data", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15))
        self.upload_user_button.pack(side="left", padx=50, pady=10)

        # upload repository data button
        self.upload_repository_button = Button(
            self.button_frame, text="Upload Repositery Data", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15))
        self.upload_repository_button.pack(side="left", padx=50, pady=10)

        # upload star data button
        self.upload_star_button = Button(
            self.button_frame, text="Upload Star Data", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15))
        self.upload_star_button.pack(side="left", padx=50, pady=10)

        # ---------- Body Frame ----------
        self.body_frame = Frame(self.parent, bg="#FFFFFF")
        self.body_frame.pack(side="top")

        # "Recommend Repositery For:" label
        self.recommend_repositery_label = Label(
            self.body_frame, text="Recommend Repositery For:", bg="#FFFFFF", font=("Arial", 12))
        self.recommend_repositery_label.grid(
            row=0, column=0, columnspan=3, padx=10, pady=0, sticky="w")

        # "Recommend Repositery" listbox
        self.recommend_repositery_listbox = Listbox(self.body_frame, width=50)
        self.recommend_repositery_listbox.grid(row=1, column=0, columnspan=2, rowspan=4,
                                               padx=(10, 0), pady=10, sticky="nsew")

        # "Recommend Repositery" scrollbar
        self.recommend_repositery_scrollbar = Scrollbar(
            self.body_frame, orient="vertical")
        self.recommend_repositery_scrollbar.grid(row=1, column=2, sticky="nsw", rowspan=4,
                                                 padx=(0, 10), pady=10)

        # "Filter by Programming Language:" label
        self.filter_by_programming_language_label = Label(
            self.body_frame, text="Filter by Programming Language:", bg="#FFFFFF", font=("Arial", 12))
        self.filter_by_programming_language_label.grid(row=5, column=0, columnspan=3,
                                                       padx=10, pady=10, sticky="w")

        # "Filter by Programming Language:" combobox
        self.filter_by_programming_language_combobox = ttk.Combobox(
            self.body_frame, width=20)
        self.filter_by_programming_language_combobox.grid(row=6, column=0, columnspan=1,
                                                          padx=10, pady=10, sticky="nswe")

        # "Number of Recommendation:" label
        self.number_of_recommendation_label = Label(
            self.body_frame, text="Number of Recommendation:", bg="#FFFFFF", font=("Arial", 12))
        self.number_of_recommendation_label.grid(row=7, column=0,
                                                 padx=(10, 0), pady=10, sticky="w")

        # "Number of Recommendation:" entry
        self.number_of_recommendation_entry = Entry(self.body_frame, width=5)
        self.number_of_recommendation_entry.grid(
            row=7, column=1, padx=(0, 10), pady=10, sticky="w")

        # "Choice Distance algorithm ↓" label
        self.distance_algorthim_label = Label(
            self.body_frame, text="Choice Distance algorithm ↓", bg="#FFFFFF", font=("Arial", 12))
        self.distance_algorthim_label.grid(
            row=0, column=3, padx=10, pady=10, sticky="nsew")

        # euclidean checkbox
        self.euclidean_checkbox = ttk.Checkbutton(
            self.body_frame, text="Euclidean", onvalue=1, offvalue=0)
        self.euclidean_checkbox.grid(
            row=1, column=3, padx=10, pady=10, sticky="nsew")

        # pearson checkbox
        self.pearson_checkbox = ttk.Checkbutton(
            self.body_frame, text="Pearson", onvalue=1, offvalue=0)
        self.pearson_checkbox.grid(
            row=2, column=3, padx=10, pady=10, sticky="nsew")

        # recommend button
        self.recommend_button = Button(
            self.body_frame, text="Recommend", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15))
        self.recommend_button.grid(
            row=3, column=3, padx=10, pady=10, sticky="nsew")

        # recommend github button
        self.recommend_github_button = Button(
            self.body_frame, text="Recommend Github", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15))
        self.recommend_github_button.grid(
            row=4, column=3, padx=10, pady=10, sticky="nsew")

        # recommendetions label
        self.recommendetions_label = Label(
            self.body_frame, text="Recommendations", bg="#FFFFFF", font=("Arial", 12))
        self.recommendetions_label.grid(row=0, column=4, columnspan=2,
                                        padx=10, pady=10, sticky="nsew")

        # recommendetions listbox
        self.recommendetions_listbox = Listbox(self.body_frame, width=50)
        self.recommendetions_listbox.grid(row=1, column=4, rowspan=4, padx=(
            10, 0), pady=10, sticky="nsew")

        # recommendetions listbox scrollbar
        self.recommendetions_scrollbar = Scrollbar(
            self.body_frame, orient="vertical")
        self.recommendetions_scrollbar.grid(row=1, column=5,  sticky="nsw", rowspan=4,
                                            padx=(0, 10), pady=10)

        self.author_label = Label(
            self.body_frame, text="Devoleped by ❤ Mehmet Jank ", bg="#FFFFFF", font=("Arial", 8))
        self.author_label.grid(
            row=7, column=4, columnspan=2, sticky="se")


def main():
    root = Tk()
    root.geometry("900x475")
    root.title("Recommender System")
    root.resizable(False, False)
    root.config(bg="#F5F5F5")
    app = Gui(root)
    root.mainloop()


main()
