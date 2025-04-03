
booksCollection = []

def registerBook(title, author, year, isbn, category):
    books = {} 
    books[isbn] = {  
        'title': title,  
        'author': author, 
        'year': year,     
        'category': category 
    }
    return booksCollection.append(books[isbn]) 


def searchByTitle (title) : 
    for book in booksCollection:
        if book['title'].lower() == title.lower():
            return book
    return None    

def searchByAuthor(author):
    for book in booksCollection:
        if book['author'].lower() == author.lower():
            return book
    return None

def searchByCategory(category):
    for book in booksCollection:
        if book['category'].lower() == category.lower():
            return book
    return None

def saveBooksToFile (filename) :
    with open(filename, 'w',encoding='utf-8') as file:
        for book in booksCollection:
            file.write(f"Title: {book['title']}\n")
            file.write(f"Author: {book['author']}\n")
            file.write(f"Year: {book['year']}\n")
            file.write(f"Category: {book['category']}\n")
            file.write("-" * 30 + "\n") 
    file.close()   

registerBook("The Catcher in the Rye", "J.D. Salinger", 1951, "1234567890", "Fiction")
registerBook("1984", "George Orwell", 1949, "0987654321", "Dystopian")
registerBook("To Kill a Mockingbird", "Harper Lee", 1960, "1122334455", "Fiction")
registerBook("Pride and Prejudice", "Jane Austen", 1813, "2233445566", "Romance")
registerBook("The Great Gatsby", "F. Scott Fitzgerald", 1925, "3344556677", "Classic")
registerBook("Moby-Dick", "Herman Melville", 1851, "4455667788", "Adventure",)
registerBook("War and Peace", "Leo Tolstoy", 1869, "5566778899", "Historical")
registerBook("The Odyssey", "Homer", -800, "6677889900", "Epic")
registerBook("Ulysses", "James Joyce", 1922, "7788990011", "Modernist")
registerBook("The Brothers Karamazov", "Fyodor Dostoevsky", 1880, "8899001122", "Philosophical")
registerBook("Crime and Punishment", "Fyodor Dostoevsky", 1866, "9900112233", "Psychological")
registerBook("Brave New World", "Aldous Huxley", 1932, "0011223344", "Dystopian")
registerBook("The Hobbit", "J.R.R. Tolkien", 1937, "1122334455", "Fantasy")
registerBook("The Picture of Dorian Gray", "Oscar Wilde", 1890, "2233445566", "Gothic")
registerBook("Dracula", "Bram Stoker", 1897, "3344556677", "Horror")
registerBook("The Lord of the Rings", "J.R.R. Tolkien", 1954, "4455667788", "Fantasy")
registerBook("Les Misérables", "Victor Hugo", 1862, "5566778899", "Historical")
registerBook("The Divine Comedy", "Dante Alighieri", 1320, "6677889900", "Epic")
registerBook("Anna Karenina", "Leo Tolstoy", 1878, "7788990011", "Tragedy")
registerBook("Frankenstein", "Mary Shelley", 1818, "8899001122", "Gothic")


saveBooksToFile("acervo_de_livros.txt")








