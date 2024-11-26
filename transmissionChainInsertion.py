import NarratorsGraph

#chain_index:int
#current_narrator:Narrator
#chains_data:dictionary (result of prepare_chains)
#narrators_graph: GrapheDeNarrateurs


#check_narrator:Ensure that no narrator name is repeated at any level.
def check_narrator(chain_index,current_narrator,chains_data):
    current_list=chains_data[chain_index]
    current_narrator_index=len(current_list)
    for chain in chains_data.values():
        if chain.len()>=current_narrator_index:
            if current_narrator.name==chain[current_narrator_index]:
                print("Ce narrateur existe déjà à ce niveau ")
                return
            

#adds a given narrator(current_narrator) to a given chain(indexed by chain_index)
def add_narrator_to_chain(chain_index,current_narrator,chains_data,narrators_graph):
    current_narrator_index=len(chains_data[chain_index])

    check_narrator(chain_index,current_narrator,chains_data)

    narrators_graph.ajouter_narrateur(current_narrator)

    last_narrator_of_current_chain=chains_data[chain_index][current_narrator_index-1]
    narrators_graph.ajouter_connexion(last_narrator_of_current_chain,current_narrator.name)


#adds a transmission chain to the chains dictionary(chains_dict)
def add_chain_to_graph(chain_index,current_chain,chains_dict):
    for narrator in current_chain:
        check_narrator(chain_index,narrator,chains_dict)

    chains_dict[chain_index]=current_chain

