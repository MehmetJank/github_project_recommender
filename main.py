# Author: Mehmet Can KAYA
# Student ID: 211216058

# recommendation.py dosyasında bulunan fonksiyonlar kullanılarak kullanıcıya ve repoya göre tavsiyelerde bulunulmuştur.
# guncel recommendation.py dosyası ile çalismaktadir.
from recommendations import *

#
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
    IntVar,
)


class ReadData:
    """ReadData class for read data from files"""

    def load_user_data(self):
        """open file dialog to select user data file"""
        self.file_path = filedialog.askopenfilename(
            title="Select User Data File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if self.file_path:
            with open(self.file_path, 'r') as user_data_file:
                lines = user_data_file.readlines()
                user_data = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        user_info = line.split(',')
                        user = {
                            'id': int(user_info[0]),
                            'username': user_info[1],
                            'github_url': user_info[2]
                        }
                        user_data.append(user)
                # Username sorting alphabetically
                user_data.sort(key=lambda x: x['username'])
        return user_data

    def load_star_data(self):
        """open file dialog to select star data file"""
        self.file_path = filedialog.askopenfilename(
            title="Select Star Data File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if self.file_path:
            with open(self.file_path, 'r') as star_data_file:
                lines = star_data_file.readlines()
                star_data = {}
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('\t')
                        star_id = int(parts[0])
                        repositories = [int(repo_id)
                                        for repo_id in parts[1].split(',')]
                        # give 5.0 score for each repository
                        star_data[star_id] = {
                            repo_id: 5.0 for repo_id in repositories}
            return star_data

    def load_repository_data(self):
        """open file dialog to select repository data file"""
        self.file_path = filedialog.askopenfilename(
            title="Select Repositery Data File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if self.file_path:
            with open(self.file_path, 'r') as repository_data_file:
                lines = repository_data_file.readlines()
                repository_data = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        repo_info = line.split(',')
                        repository = {
                            'id': int(repo_info[0]),
                            'repository_name': repo_info[1],
                            'url': repo_info[2],
                            'language': repo_info[3]
                        }
                        repository_data.append(repository)
            return repository_data


class Recommend:
    """Recommend class for recommend repositories and users"""

    def __init__(self, user_data, repository_data, star_data):
        self.user_data = user_data
        self.repository_data = repository_data
        self.star_data = star_data

    def get_repository_preferences(self):
        """get repository preferences"""
        repository_preferences = {}
        for star_id, repositories in self.star_data.items():
            for repository_id in repositories:
                repository_preferences.setdefault(repository_id, {})
                repository_preferences[repository_id][star_id] = 5
        return repository_preferences

    def recommend_repositories(self, user_id, repository_preferences, similarity, language_filter=None, n=5):
        """recommend repositories"""
        repository_preferences = self.get_repository_preferences()
        transformed_prefs = transformPrefs(repository_preferences)

        if similarity == 'euclidean':
            sim_func = sim_distance
        elif similarity == 'pearson':
            sim_func = sim_pearson

        if language_filter == "None":
            language_filter = None

        recommendations = getRecommendations(
            transformed_prefs, user_id, similarity=sim_func)

        if language_filter:
            recommendations = [(score, repo_id) for score, repo_id in recommendations if
                               self.repository_data[repo_id]['language'] == language_filter]

        return recommendations[:n]

    def recommend_users(self, user_id, similarity='euclidean', n=5):
        """recommend users"""
        user_prefs = {user_id: {repo_id: 5 for repo_id in repo_list}
                      for user_id, repo_list in self.star_data.items()}

        if similarity == 'euclidean':
            sim_func = sim_distance
        elif similarity == 'pearson':
            sim_func = sim_pearson

        user_recommendations = topMatches(
            user_prefs, user_id, n=n, similarity=sim_func)
        return user_recommendations


class Gui(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.euclidean_checkbox_var = IntVar()
        self.pearson_checkbox_var = IntVar()
        self.initUI()

    def load_data(self, routes: str):
        """load data from files"""
        if routes == "load_user_data":
            self.user_data = ReadData().load_user_data()
            self.recommend_repositery_listbox.delete(0, END)
            self.recommend_repositery_listbox_tree_view.delete(
                *self.recommend_repositery_listbox_tree_view.get_children())

            if self.user_data:
                for user in self.user_data:
                    self.recommend_repositery_listbox.insert(
                        END, f"ID: {user['id']}, Username: {user['username']}")
                    self.recommend_repositery_listbox_tree_view.insert(
                        "", "end", values=(user['username'], user['id']))
            else:
                self.recommend_repositery_listbox.insert(
                    END, "No user data found")

        elif routes == "load_star_data":
            self.star_data = ReadData().load_star_data()

        elif routes == "load_repository_data":
            self.repository_data = ReadData().load_repository_data()
            self.repositery_data = {
                repository['id']: repository for repository in self.repository_data}
            programming_languages = [repository['language']
                                     for repository in self.repository_data]
            programming_languages.append(None)
            self.filter_by_programming_language_combobox['values'] = programming_languages
            self.filter_by_programming_language_combobox.current(
                len(programming_languages) - 1)

    def get_recommendations(self, process: str):
        """get recommendations"""
        self.recommendetions_listbox.delete(0, END)
        self.recommendetions_listbox_tree_view.delete(
            *self.recommendetions_listbox_tree_view.get_children())

        if self.euclidean_checkbox_var.get() == 1:
            similarity = "euclidean"
        elif self.pearson_checkbox_var.get() == 1:
            similarity = "pearson"
        else:
            similarity = "euclidean"

        self.recommendation_user_id = self.recommend_repositery_listbox_tree_view.item(
            self.recommend_repositery_listbox_tree_view.selection())['values'][1]
        self.recommendation_number = self.number_of_recommendation_entry.get()

        if not self.recommendation_number:
            self.recommendation_number = None
        else:
            self.recommendation_number = int(self.recommendation_number)

        self.recommendation_filter = self.filter_by_programming_language_combobox.get()

        # hasattr function checks if the object has the given named attribute and return True if present, else False.
        if hasattr(self, 'repository_data') and hasattr(self, 'star_data') and hasattr(self, 'user_data'):
            recommender = Recommend(
                self.user_data, self.repository_data, self.star_data)

            if process == "recommend_repo":
                recommendations = recommender.recommend_repositories(
                    self.recommendation_user_id, recommender.get_repository_preferences(), similarity, self.recommendation_filter, self.recommendation_number)
            elif process == "recommend_user":
                recommendations = recommender.recommend_users(
                    self.recommendation_user_id, similarity, self.recommendation_number)

            if recommendations:
                if process == "recommend_repo":
                    for score, repo_id in recommendations:
                        repository = self.repository_data[repo_id]
                        self.recommendetions_listbox.insert(
                            END, f"Name: {repository['repository_name']}, URL: {repository['url']}, Score: {score}")
                        self.recommendetions_listbox_tree_view.insert(
                            "", "end", values=(repository['repository_name'], repository['url'], score))
                elif process == "recommend_user":
                    for score, recommended_user_id in recommendations:
                        recommended_user = self.user_data[recommended_user_id]
                        self.recommendetions_listbox.insert(
                            END, f"ID: {recommended_user['id']}, Username: {recommended_user['username']}, Score: {score}")
                        self.recommendetions_listbox_tree_view.insert(
                            "", "end", values=(recommended_user['username'], recommended_user['id'], score))
            else:
                # if no recommendation found then add "No recommendation found" to listbox
                self.recommendetions_listbox.insert(
                    END, "No recommendation found")
                self.recommendetions_listbox_tree_view.insert(
                    "", "end", values=("", "No recommendation found", ""))
        else:
            messagebox.showerror(
                "Error", "Please upload all required data first.")

    def check(self, checkbox):
        """checkbox selection change. Only one checkbox can be selected at a time"""
        if checkbox == "euclidean":
            if self.euclidean_checkbox_var.get() == 1:
                self.pearson_checkbox_var.set(0)
        elif checkbox == "pearson":
            if self.pearson_checkbox_var.get() == 1:
                self.euclidean_checkbox_var.set(0)

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
            self.button_frame, text="Upload User Data", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15), command=lambda: self.load_data("load_user_data"))
        self.upload_user_button.pack(side="left", padx=50, pady=10)

        # upload repository data button
        self.upload_repository_button = Button(
            self.button_frame, text="Upload Repositery Data", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15), command=lambda: self.load_data("load_repository_data"))
        self.upload_repository_button.pack(side="left", padx=50, pady=10)

        # upload star data button
        self.upload_star_button = Button(
            self.button_frame, text="Upload Star Data", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15), command=lambda: self.load_data("load_star_data"))
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

        # "Recommend Repositery" listbox tree view
        self.recommend_repositery_listbox_tree_view = ttk.Treeview(self.body_frame, columns=(
            "User Name", "User ID"), show="headings", height=5)
        self.recommend_repositery_listbox_tree_view.column(
            "User Name", width=90)
        self.recommend_repositery_listbox_tree_view.column("User ID", width=5)
        self.recommend_repositery_listbox_tree_view.heading(
            "User Name", text="User Name")
        self.recommend_repositery_listbox_tree_view.heading(
            "User ID", text="User ID")
        self.recommend_repositery_listbox_tree_view.grid(
            row=1, column=0, columnspan=2, rowspan=4, padx=(10, 0), pady=10, sticky="nsew")

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
            self.body_frame, text="Euclidean", variable=self.euclidean_checkbox_var, onvalue=1, offvalue=0, command=lambda: self.check("euclidean"))
        self.euclidean_checkbox.grid(
            row=1, column=3, padx=10, pady=10, sticky="nsew")

        # pearson checkbox
        self.pearson_checkbox = ttk.Checkbutton(
            self.body_frame, text="Pearson", variable=self.pearson_checkbox_var, onvalue=1, offvalue=0, command=lambda: self.check("pearson"))
        self.pearson_checkbox.grid(
            row=2, column=3, padx=10, pady=10, sticky="nsew")

        # recommend button
        self.recommend_button = Button(
            self.body_frame, text="Recommend Repo", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15), command=lambda: self.get_recommendations("recommend_repo"))

        self.recommend_button.grid(
            row=3, column=3, padx=10, pady=10, sticky="nsew")

        # recommend user button
        self.recommend_user_button = Button(
            self.body_frame, text="Recommend User", bg="#FFAE00", fg="#FFFFFF", font=("Arial", 15), command=lambda: self.get_recommendations("recommend_user"))
        self.recommend_user_button.grid(
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

        # "Recommendations" listbox tree view
        self.recommendetions_listbox_tree_view = ttk.Treeview(self.body_frame, columns=(
            "Name", "URL", "Score"), show="headings", height=5)
        self.recommendetions_listbox_tree_view.column("Name", width=10)
        self.recommendetions_listbox_tree_view.column("URL", width=100)
        self.recommendetions_listbox_tree_view.column("Score", width=10)
        self.recommendetions_listbox_tree_view.heading(
            "Name", text="Name")
        self.recommendetions_listbox_tree_view.heading(
            "URL", text="URL")
        self.recommendetions_listbox_tree_view.heading(
            "Score", text="Score")
        self.recommendetions_listbox_tree_view.grid(
            row=1, column=4, rowspan=4, padx=(10, 0), pady=10, sticky="nsew")

        # recommendetions listbox scrollbar
        self.recommendetions_scrollbar = Scrollbar(
            self.body_frame, orient="vertical")
        self.recommendetions_scrollbar.grid(row=1, column=5,  sticky="nsw", rowspan=4,
                                            padx=(0, 10), pady=10)

        # Author label
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
