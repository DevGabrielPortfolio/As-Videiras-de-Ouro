from flask import Flask, render_template, redirect, request, flash, url_for, get_flashed_messages, session
from functools import wraps

from models.category_controller import Categories
from models.wine_controller import Wines
from models.shopping_cart_controller import ControlShoppingCart
from models.comments_controller import Comments

app = Flask(__name__)

app.secret_key = 'sua_chave_secreta_super_segura_aqui_12345'




def login_required(f):
    """
    Decorador para garantir que o usuário esteja logado para acessar certas rotas.
    Redireciona para a página de login se o user_id não estiver na sessão.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'info')
            return redirect(url_for('login'))  # Redireciona para a rota de login
        return f(*args, **kwargs)

    return decorated_function


@app.route('/logout')
def logout():
    """
    Rota para deslogar o usuário.
    Remove o user_id e username da sessão e redireciona para a página principal.
    """
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Você foi desconectado com sucesso.', 'success') # Adiciona uma mensagem de sucesso ao deslogar
    return redirect(url_for('main_page'))





@app.route('/')
def main_page():
    """
    Rota da página principal que exibe categorias e vinhos.
    Permite filtrar vinhos por categoria.
    """
    categorias = Categories.get_all_categories()

    category_id = request.args.get('categoria', type=int)

    vinhos = []
    if category_id:
        vinhos = Wines.get_wines_by_category(category_id)
        if not vinhos:
            flash(f'Nenhum vinho encontrado para a categoria selecionada.', 'info')
    else:
        vinhos = Wines.get_all_wines()
        if not vinhos:
            flash('Nenhum vinho cadastrado no momento.', 'info')

    return render_template('home.html', categorias=categorias, produtos=vinhos)



@app.route('/configuracoes-conta')
def create_acount():
    """
    Rota para a página de criação de conta/configurações.
    """
    return render_template('create_account_page.html')



@app.route('/carrinho')
@login_required
def carrinho():
    """
    Rota para exibir o carrinho de compras do usuário logado.
    """
    id_usuario = session['user_id']
    # A verificação de id_usuario já é feita pelo decorador login_required
    # if not id_usuario:
    #     flash('Você precisa estar logado para ver seu carrinho.', 'danger')
    #     return redirect(url_for('login'))

    itens_carrinho = ControlShoppingCart.get_itens_carrinho_por_usuario(id_usuario)
    total_carrinho = sum(item['preco_unitario'] * item['quantidade'] for item in itens_carrinho)
    return render_template('cart.html', itens_carrinho=itens_carrinho, total_carrinho=total_carrinho)



@app.route('/vinho/<int:vinho_id>')
def detalhes_vinho(vinho_id):
    """
    Rota para exibir os detalhes de um vinho específico, incluindo comentários.
    """
    print(f"DEBUG: Tentando buscar detalhes para o vinho_id = {vinho_id}")
    vinho = Wines.get_wine_by_id(vinho_id)
    if vinho:
        categorias = Categories.get_all_categories()

        # CHAME A FUNÇÃO PARA BUSCAR OS COMENTÁRIOS AQUI
        comentarios = Comments.get_comments_by_product_id(vinho_id)

        # PASSE OS COMENTÁRIOS PARA O TEMPLATE
        return render_template('wine_details.html', 
                               vinho=vinho, 
                               categorias=categorias, 
                               comentarios=comentarios, 
                               id_produto=vinho_id) 
    else:
        flash('Vinho não encontrado.', 'danger')
        return redirect(url_for('main_page'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)