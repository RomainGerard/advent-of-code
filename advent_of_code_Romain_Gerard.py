import numpy as np

# Solutions:
    # PB 1: 2742123   (e1), 21328497 (e2)
    # PB 2: 479       (e1), 531      (e2)
    # PB 3: 166905464 (e1), 72948684 (e2)
    # PB 4: 2504      (e1), 1923     (e2)

# Si l'on souhaite resoudre un probleme precis il suffit de changer 'pb_nb' et 'star_nb' dans l'instanciation de Problem_Solving en fin de code

# ATTENTION: les fichiers input on vu leurs noms modifies en 'input_pb{i}.txt' ou i est l'indice du pb (de 1 a 4)

class Problem_Solving:
    #============================================================================================
    # Initialisation et fonction de choix du pb a resoudre

    def __init__(self, pb_nb=1, star_nb=1):
        self.pb_nb = pb_nb
        self.star_nb = star_nb

    def solve_pb(self) -> None:
        answer = -1
        if self.pb_nb == 1:
            answer = self.solve_pb_1()
        
        elif self.pb_nb == 2:
            answer = self.solve_pb_2()

        elif self.pb_nb == 3:
            answer = self.solve_pb_3()
        
        else:
            answer = self.solve_pb_4()
        
        print(answer)

    #============================================================================================
    # PB 1

    def solve_pb_1(self) -> int:
        # On ouvre le fichier puis on en stocke les infos dans la matrice numbers
        with open("input_pb1.txt", "r", encoding="utf-8") as file:
            LINES = file.readlines() 

        numbers = np.zeros((2, len(LINES)), dtype=int)

        for i,line in enumerate(LINES):
            line_nb = ['', '']
            # on remplit d'abord l'entier de gauche
            left_or_right = 0

            for char in line:
                if char.isdigit():
                    line_nb[left_or_right] += char
                else: # si le char est un espace alors on passe au remplissage de l'entier de droite
                    left_or_right = 1

            numbers[:,i] = int(line_nb[0]) , int(line_nb[1])

        answer = -1
        #_______________________________________________________
        # Etoile n.1 : 
        if self.star_nb == 1:
            numbers[0].sort()
            numbers[1].sort()

            answer = np.abs(numbers[0]-numbers[1]).sum()
        
        #_______________________________________________________
        # Etoile n.2 : 
        else:
            answer = 0
            for i in range(len(LINES)):
                left_nb = numbers[0][i]
                answer += left_nb*np.count_nonzero(numbers[1] == left_nb)

        return answer


    #============================================================================================
    # PB 2
    
    def test_report(self, report: list) -> bool:
        valid = True

        # on ne sait pas encore a ce stade si la liste est croissante ou decroissante, le but c'est qu'elle reste au moins l'un des deux
        increasing = True
        decreasing = True

        for i in range(len(report)-1):
            level = report[i]
            next_level = report[i+1]

            if next_level-level > 0:
                if next_level-level > 3:
                    valid = False
                    break
                else: # si le report est croissant (jusqu'ici) alors il n'est pas decroissant
                    decreasing = False
            
            # pareil pour le cas decroissant
            elif next_level-level < 0:
                if next_level-level < -3:
                    valid = False
                    break
                else:
                    increasing = False
            
            # si l'ecart entre level et next_level est ni >0, ni <0, alors level = next_level ce qui n'est pas autorise
            else:
                valid = False
                break

            # cas ou le report admettrait une phase croissante et une phase decroissante
            if not (increasing or decreasing):
                valid = False
                break
        
        return valid
    

    def error_damping_naive(self, report: list) -> bool:
        # j'ai appele cette methode naive car elle est en O(nb_level^2), on pourrait potentiellement la reduire en O( nb_level)
        # en detectant quel level retirer (mais ca demande une detection un peu laborieuse et moins elegante en terme de code)
        valid = self.test_report(report)
        # si le report n'est pas valide tel quel alors on test la validite des sous-report en faisant un pop sur un des elements jusqu'a ce que ca marche
        if not valid:
            for i in range(len(report)):
                damped_report = report.copy()
                damped_report.pop(i)
                valid = self.test_report(damped_report)

                if valid:
                    break
                    
        return valid


    def solve_pb_2(self) -> int:
        
        with open("input_pb2.txt", "r", encoding="utf-8") as file:
            REPORTS = file.readlines()  # Chaque ligne est un élément de la liste


        answer = 0
        for txt_report in REPORTS:

            # Premierement on stocke les donnees
            report= []
            level = ''
            for char in txt_report:
                if char.isdigit():
                    level += char
                else:
                    report.append(int(level))
                    level = ''
            
            
            # Ensuite on verifie si le report est admissible
            #_______________________________________________________
            # Etoile n.1 : 
            if self.star_nb == 1:
                if self.test_report(report):
                    answer += 1
            #_______________________________________________________
            # Etoile n.2 : 
            else:
                if self.error_damping_naive(report):
                    answer += 1

        return answer


    #============================================================================================
    # PB 3

    def detect_mul_X_Y(self, LINES: list) -> int:
        string_to_reproduce = "mul("

        # seulement utile pour l'etoile n.2
        do = "do()"
        dont = "don't()"
        do_add = True

        answer = 0
        for line in LINES:
            X_txt = ''
            Y_txt = ''
            phase = 0 # 3 phases a detecter: 'mul(' -> 'X' (-> transition avec un ',') ->  'Y' ( -> completion avec un ')' )
            char_idx_do = 0
            char_idx_dont = 0                    
            char_idx_mul = 0

            for char in line:
                start_over = False

                # (etoile n.2) detection des do 
                if char == do[char_idx_do]:
                    if char_idx_do == len(do) - 1:
                        do_add = True
                        char_idx_do = 0
                    else:
                        char_idx_do += 1
                else:
                    char_idx_do = 0

                # (etoile n.2) detection des dont
                if char == dont[char_idx_dont]:
                    if char_idx_dont == len(dont) - 1:
                        do_add = False
                        char_idx_dont = 0
                    else:
                        char_idx_dont += 1
                else:
                    char_idx_dont = 0
            
                # 1ere etape: detection des "mul("
                if phase == 0: 
                    if char == string_to_reproduce[char_idx_mul]:
                        if char_idx_mul == len(string_to_reproduce) - 1:
                            phase = 1
                        else:
                            char_idx_mul +=1
                    else:
                        start_over = True
                # 2eme etape: detection du X et passage au Y si le charactere est ','
                elif phase == 1:
                    if char.isdigit():
                        X_txt += char
                    elif char == ',': # transition vers le Y des qu'on detecte le ','
                        phase = 2
                    else: 
                        start_over = True
                # 3eme etape: detection du Y et validation si le charactere est ')'
                elif phase == 2:
                    if char.isdigit():
                        Y_txt += char
                    else: 
                        if char == ')': # completion des qu'on detecte le ')' final
                            if self.star_nb == 1 or do_add: # soit on est dans le cas de l'etoile 1 soit on est en etoile 2 et on verifie si l'instruction est a "do"
                                answer += int(X_txt)*int(Y_txt)
                        start_over = True

                # reinitialisation des variables de checking
                if start_over:
                    X_txt = ''
                    Y_txt = ''
                    phase = 0
                    char_idx_mul = 0

        return answer
    


    def solve_pb_3(self) -> int:
        with open("input_pb3.txt", "r", encoding="utf-8") as file:
            LINES = file.readlines()  # Chaque ligne est un élément de la liste

        return self.detect_mul_X_Y(LINES)

    #============================================================================================
    # PB 4

    #_______________________________________________________
    # Etoile n.1 :

    def rec_XMAS(self, XMAS_matrix: list, i: int, j: int, step: int, direction = None) -> int:
        # Fonction qui commence par checker si on est sur un X et qui explore recursivement la recherche des XMAS dans les 8 directions
        
        XMAS_string = 'XMAS'

        n = len(XMAS_matrix)
        m = len(XMAS_matrix[0])
        # si on atteint le bord dans avoir pu completer le 'XMAS' alors on n'incremente pas le nb de XMAS trouves
        if (i < 0 or i==n) or (j<0 or j==m):
            return 0
        

        char_i_j = XMAS_matrix[i][j]
        if char_i_j == XMAS_string[step]:
            if step == 3: # ie si char_i_j == 'S'
                return 1
            else:
                if step == 0: # si on en est au 'X' alors on lance la recherche dans les 8 directions
                    return (  self.rec_XMAS(XMAS_matrix, i-1, j-1, step+1, direction=(-1,-1)) 
                            + self.rec_XMAS(XMAS_matrix, i-1, j,   step+1, direction=(-1,0)) 
                            + self.rec_XMAS(XMAS_matrix, i-1, j+1, step+1, direction=(-1,1)) 

                            + self.rec_XMAS(XMAS_matrix, i,   j+1, step+1, direction=(0,1)) 

                            + self.rec_XMAS(XMAS_matrix, i+1, j+1, step+1, direction=(1,1)) 
                            + self.rec_XMAS(XMAS_matrix, i+1, j,   step+1, direction=(1,0)) 
                            + self.rec_XMAS(XMAS_matrix, i+1, j-1, step+1, direction=(1,-1)) 

                            + self.rec_XMAS(XMAS_matrix, i,   j-1, step+1, direction=(0,-1)) )
                else: # sinon (on en est au 'M' ou au 'A' et) on poursuit dans la direction deja etablie
                    return self.rec_XMAS(XMAS_matrix, i+direction[0],   j+direction[1], step+1, direction)

        # si la lettre ne correspond pas a celle attendue alors on ne comptabilise pas car on n'a pas pu trouver le 'XMAS' dans l'ordre voulu
        else:
            return 0
        
    #_______________________________________________________
    # Etoile n.2 : 

    def star2_X_MAS(self, XMAS_matrix: list) -> int:
        # fonction qui detecte les voisins diagonaux des 'A' et qui check s'ils ont la bonne allure
        answer = 0

        n = len(XMAS_matrix)
        m = len(XMAS_matrix[0])
        for i in range(1,n-1):
            for j in range(1,m-1):

                char_i_j = XMAS_matrix[i][j]
                if char_i_j == 'A':
                    string_MMSS = XMAS_matrix[i-1][j-1] + XMAS_matrix[i+1][j-1] + XMAS_matrix[i+1][j+1] + XMAS_matrix[i-1][j+1]
                    if string_MMSS in ['MMSS', 'SMMS', 'SSMM', 'MSSM']:
                        answer +=1
        
        return answer
        

    def solve_pb_4(self) -> int:

        with open("input_pb4.txt", "r", encoding="utf-8") as file:
            LINES = file.readlines()  
            
        XMAS_mat = []
        for line in LINES:
            row = []
            for char in line:
                if char != '\n':
                    row.append(char)
            XMAS_mat.append(row.copy())

        answer = 0
        #_______________________________________________________
        # Etoile n.1 : 
        if self.star_nb == 1:
            n = len(XMAS_mat)
            m = len(XMAS_mat[0])
            for i in range(n):
                for j in range(m):
                    answer += self.rec_XMAS(XMAS_mat, i,j,0)
        #_______________________________________________________
        # Etoile n.2 :         
        else:
            answer = self.star2_X_MAS(XMAS_mat)
        
        return answer



# Choix du pb a resoudre
if __name__ == "__main__":
    pb_solved = Problem_Solving(pb_nb=4,star_nb=2)

    pb_solved.solve_pb()
