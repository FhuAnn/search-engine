class InvertedIndex:
    def __init__(self):
        self.index ={}
    
    def add_document(self, document_id,document):
        terms = document.split() #apple banana apple -> ['apple','banana','apple']
        for position, term in enumerate(terms): #position -> 0 , apple-->1 
            if term not in self.index:
                self.index[term] = {}
                if document_id not in self.index[term]:
                    self.index[term][document_id] = []

                self.index[term][document_id].append(position)

    def search(self,query):
        terms = query.split()
        results = None
        for term in terms:
            if term in self.index:
                if results is None:
                    results = set(self.index[term].keys())
                else:
                    results.intersection_update(self.index[term].keys())
                if results is None: 
                    return []
                else:
                    search_results = []  
                    for document_id in results:
                        positions = [self.index[term][document_id] for term in terms]
                        search_results.append((document_id,positions))

                    return search_results

index = InvertedIndex()

index.add_document(1,'apple banana apple')
index.add_document(2,"banana cherry")
index.add_document(3,"apple cherry")

print("Documents added to the inverted index")
print(index.index)

query ="apple"

search_result = index.search(query)

print(f"Search result for '{query}': ")

if search_result == []:
    print("Not found")
for document_id,positions in search_result:
    print(f"Document Id: {document_id}")
    print(f"Position: {positions}")