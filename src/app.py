from __future__ import annotations

from datetime import date, datetime

import streamlit as st

try:
    from src.database import SessionLocal, initialize_database
    from src.models import (
        Brand,
        Category,
        Client,
        Clothing,
        Employee,
        Sale,
        SaleItem,
        StockEntry,
        StockEntryItem,
        Supplier,
        Variation,
    )
except ImportError:  # pragma: no cover
    from database import SessionLocal, initialize_database
    from models import (
        Brand,
        Category,
        Client,
        Clothing,
        Employee,
        Sale,
        SaleItem,
        StockEntry,
        StockEntryItem,
        Supplier,
        Variation,
    )

st.set_page_config(page_title="Loja de Roupas", page_icon="👕", layout="wide")
initialize_database()


def delete_record(model, record_id):
    with SessionLocal() as session:
        obj = session.get(model, record_id)
        if obj is not None:
            session.delete(obj)
            session.commit()
            st.success("Registro removido com sucesso!")


def get_summary():
    with SessionLocal() as session:
        return {
            "categorias": session.query(Category).count(),
            "marcas": session.query(Brand).count(),
            "roupas": session.query(Clothing).count(),
            "variacoes": session.query(Variation).count(),
            "clientes": session.query(Client).count(),
            "funcionarios": session.query(Employee).count(),
            "fornecedores": session.query(Supplier).count(),
            "vendas": session.query(Sale).count(),
        }


def render_summary():
    st.title("Sistema de Gerenciamento de Roupas")
    st.subheader("Controle de estoque, marcas, clientes e vendas")
    stats = get_summary()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Categorias", stats["categorias"])
    col2.metric("Marcas", stats["marcas"])
    col3.metric("Roupas", stats["roupas"])
    col4.metric("Variações", stats["variacoes"])
    col5.metric("Vendas", stats["vendas"])

    st.markdown("### Visão geral")
    st.info(
        "Este sistema organiza o cadastro de roupas, categorias, marcas, clientes, funcionários, fornecedores, vendas e entradas de estoque."
    )


def render_categories():
    st.title("CRUD de Categorias")

    with SessionLocal() as session:
        categorias = session.query(Category).order_by(Category.id.desc()).all()

    selected_id = st.selectbox(
        "Editar categoria existente",
        [0] + [categoria.id for categoria in categorias],
        format_func=lambda value: "Nova categoria" if value == 0 else f"Categoria {value}",
    )

    current = None
    if selected_id:
        current = next((c for c in categorias if c.id == selected_id), None)

    with st.form("form_categoria"):
        name = st.text_input("Nome", value=current.name if current else "")
        description = st.text_area("Descrição", value=current.description if current else "")
        is_active = st.checkbox("Ativa", value=current.is_active if current else True)
        submitted = st.form_submit_button("Salvar categoria")

    if submitted:
        with SessionLocal() as session:
            if selected_id:
                item = session.get(Category, selected_id)
                if item:
                    item.name = name.strip()
                    item.description = description.strip() or None
                    item.is_active = is_active
                    session.commit()
                    st.success("Categoria atualizada com sucesso!")
            else:
                if name.strip():
                    session.add(
                        Category(
                            name=name.strip(),
                            description=description.strip() or None,
                            is_active=is_active,
                        )
                    )
                    session.commit()
                    st.success("Categoria cadastrada com sucesso!")
                else:
                    st.warning("Informe o nome da categoria.")
            st.rerun()

    st.markdown("### Lista de categorias")
    if not categorias:
        st.write("Nenhuma categoria cadastrada.")
        return

    for item in categorias:
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{item.name}**")
        col2.write(f"Status: {'Ativa' if item.is_active else 'Inativa'}")
        if col3.button("Excluir", key=f"del-cat-{item.id}"):
            delete_record(Category, item.id)
            st.rerun()


def render_brands():
    st.title("CRUD de Marcas")

    with SessionLocal() as session:
        marcas = session.query(Brand).order_by(Brand.id.desc()).all()

    selected_id = st.selectbox(
        "Editar marca existente",
        [0] + [marca.id for marca in marcas],
        format_func=lambda value: "Nova marca" if value == 0 else f"Marca {value}",
    )

    current = None
    if selected_id:
        current = next((m for m in marcas if m.id == selected_id), None)

    with st.form("form_marca"):
        name = st.text_input("Nome", value=current.name if current else "")
        description = st.text_area("Descrição", value=current.description if current else "")
        country = st.text_input("País de origem", value=current.country_of_origin if current else "")
        is_active = st.checkbox("Ativa", value=current.is_active if current else True)
        submitted = st.form_submit_button("Salvar marca")

    if submitted:
        with SessionLocal() as session:
            if selected_id:
                item = session.get(Brand, selected_id)
                if item:
                    item.name = name.strip()
                    item.description = description.strip() or None
                    item.country_of_origin = country.strip() or None
                    item.is_active = is_active
                    session.commit()
                    st.success("Marca atualizada com sucesso!")
            else:
                if name.strip():
                    session.add(
                        Brand(
                            name=name.strip(),
                            description=description.strip() or None,
                            country_of_origin=country.strip() or None,
                            is_active=is_active,
                        )
                    )
                    session.commit()
                    st.success("Marca cadastrada com sucesso!")
                else:
                    st.warning("Informe o nome da marca.")
            st.rerun()

    st.markdown("### Lista de marcas")
    if not marcas:
        st.write("Nenhuma marca cadastrada.")
        return

    for item in marcas:
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{item.name}**")
        col2.write(f"País: {item.country_of_origin or 'Não informado'}")
        if col3.button("Excluir", key=f"del-brand-{item.id}"):
            delete_record(Brand, item.id)
            st.rerun()


def render_clothes():
    st.title("CRUD de Roupas")

    with SessionLocal() as session:
        marcas = session.query(Brand).filter(Brand.is_active.is_(True)).order_by(Brand.name).all()
        categorias = session.query(Category).filter(Category.is_active.is_(True)).order_by(Category.name).all()
        roupas = session.query(Clothing).order_by(Clothing.id.desc()).all()

    selected_id = st.selectbox(
        "Editar roupa existente",
        [0] + [roupa.id for roupa in roupas],
        format_func=lambda value: "Nova roupa" if value == 0 else f"Roupa {value}",
    )

    current = None
    if selected_id:
        current = next((r for r in roupas if r.id == selected_id), None)

    with st.form("form_roupa"):
        name = st.text_input("Nome", value=current.name if current else "")
        description = st.text_area("Descrição", value=current.description if current else "")
        brand = st.selectbox(
            "Marca",
            options=[m.id for m in marcas],
            format_func=lambda value: next((m.name for m in marcas if m.id == value), "Selecione"),
            index=(next((i for i, m in enumerate(marcas) if current and m.id == current.brand_id), 0) if current else 0),
        )
        categories_selected = st.multiselect(
            "Categorias",
            options=[c.id for c in categorias],
            default=[cat.id for cat in (current.categories if current else [])],
            format_func=lambda value: next((c.name for c in categorias if c.id == value), str(value)),
        )
        price_sale = st.number_input("Preço de venda", min_value=0.01, value=current.price_sale if current else 0.0, step=0.5)
        price_cost = st.number_input("Preço de custo", min_value=0.0, value=current.price_cost if current else 0.0, step=0.5)
        is_active = st.checkbox("Ativa", value=current.is_active if current else True)
        submitted = st.form_submit_button("Salvar roupa")

    if submitted:
        with SessionLocal() as session:
            if selected_id:
                item = session.get(Clothing, selected_id)
                if item:
                    item.name = name.strip()
                    item.description = description.strip() or None
                    item.brand_id = brand
                    item.price_sale = float(price_sale)
                    item.price_cost = float(price_cost)
                    item.is_active = is_active
                    item.categories = [session.get(Category, cat_id) for cat_id in categories_selected]
                    session.commit()
                    st.success("Roupa atualizada com sucesso!")
            else:
                if name.strip():
                    if not categories_selected:
                        st.warning("A roupa deve pertencer a pelo menos uma categoria.")
                    else:
                        item = Clothing(
                            name=name.strip(),
                            description=description.strip() or None,
                            brand_id=brand,
                            price_sale=float(price_sale),
                            price_cost=float(price_cost),
                            is_active=is_active,
                        )
                        item.categories = [session.get(Category, cat_id) for cat_id in categories_selected]
                        session.add(item)
                        session.commit()
                        st.success("Roupa cadastrada com sucesso!")
                else:
                    st.warning("Informe o nome da roupa.")
            st.rerun()

    st.markdown("### Lista de roupas")
    if not roupas:
        st.write("Nenhuma roupa cadastrada.")
        return

    for item in roupas:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**{item.name}**")
        col2.write(f"Marca: {item.brand.name if item.brand else 'Sem marca'}")
        col3.write(f"Preço: R$ {item.price_sale:.2f}")
        if col4.button("Excluir", key=f"del-clothing-{item.id}"):
            delete_record(Clothing, item.id)
            st.rerun()


def render_variations():
    st.title("CRUD de Variações")

    with SessionLocal() as session:
        roupas = session.query(Clothing).order_by(Clothing.name).all()
        variacoes = session.query(Variation).order_by(Variation.id.desc()).all()

    selected_id = st.selectbox(
        "Editar variação existente",
        [0] + [v.id for v in variacoes],
        format_func=lambda value: "Nova variação" if value == 0 else f"Variação {value}",
    )

    current = next((v for v in variacoes if v.id == selected_id), None) if selected_id else None

    with st.form("form_variacao"):
        clothing_id = st.selectbox(
            "Roupa",
            options=[r.id for r in roupas],
            format_func=lambda value: next((r.name for r in roupas if r.id == value), str(value)),
            index=(next((i for i, r in enumerate(roupas) if current and r.id == current.clothing_id), 0) if current else 0),
        )
        size = st.text_input("Tamanho", value=current.size if current else "")
        color = st.text_input("Cor", value=current.color if current else "")
        stock_quantity = st.number_input("Quantidade em estoque", min_value=0, value=current.stock_quantity if current else 0, step=1)
        submitted = st.form_submit_button("Salvar variação")

    if submitted:
        with SessionLocal() as session:
            if selected_id:
                item = session.get(Variation, selected_id)
                if item:
                    item.clothing_id = clothing_id
                    item.size = size.strip()
                    item.color = color.strip()
                    item.stock_quantity = int(stock_quantity)
                    session.commit()
                    st.success("Variação atualizada com sucesso!")
            else:
                if size.strip() and color.strip():
                    session.add(
                        Variation(
                            clothing_id=clothing_id,
                            size=size.strip(),
                            color=color.strip(),
                            stock_quantity=int(stock_quantity),
                        )
                    )
                    session.commit()
                    st.success("Variação cadastrada com sucesso!")
                else:
                    st.warning("Informe tamanho e cor da variação.")
            st.rerun()

    st.markdown("### Lista de variações")
    if not variacoes:
        st.write("Nenhuma variação cadastrada.")
        return

    for item in variacoes:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**{item.clothing.name if item.clothing else 'Roupa'}**")
        col2.write(f"{item.size} / {item.color}")
        col3.write(f"Estoque: {item.stock_quantity}")
        if col4.button("Excluir", key=f"del-variation-{item.id}"):
            delete_record(Variation, item.id)
            st.rerun()


def render_clients():
    st.title("CRUD de Clientes")

    with SessionLocal() as session:
        clientes = session.query(Client).order_by(Client.id.desc()).all()

    selected_id = st.selectbox(
        "Editar cliente existente",
        [0] + [cliente.id for cliente in clientes],
        format_func=lambda value: "Novo cliente" if value == 0 else f"Cliente {value}",
    )

    current = next((c for c in clientes if c.id == selected_id), None) if selected_id else None

    with st.form("form_cliente"):
        name = st.text_input("Nome", value=current.name if current else "")
        cpf = st.text_input("CPF", value=current.cpf if current else "")
        email = st.text_input("Email", value=current.email if current else "")
        phone = st.text_input("Telefone", value=current.phone if current else "")
        birth_date = st.date_input("Data de nascimento", value=current.birth_date if current else date.today())
        address = st.text_area("Endereço", value=current.address if current else "")
        observation = st.text_area("Observação", value=current.observation if current else "")
        is_active = st.checkbox("Ativo", value=current.is_active if current else True)
        submitted = st.form_submit_button("Salvar cliente")

    if submitted:
        with SessionLocal() as session:
            if selected_id:
                item = session.get(Client, selected_id)
                if item:
                    item.name = name.strip()
                    item.cpf = cpf.strip()
                    item.email = email.strip()
                    item.phone = phone.strip() or None
                    item.birth_date = birth_date
                    item.address = address.strip() or None
                    item.observation = observation.strip() or None
                    item.is_active = is_active
                    session.commit()
                    st.success("Cliente atualizado com sucesso!")
            else:
                if name.strip() and cpf.strip() and email.strip():
                    session.add(
                        Client(
                            name=name.strip(),
                            cpf=cpf.strip(),
                            email=email.strip(),
                            phone=phone.strip() or None,
                            birth_date=birth_date,
                            address=address.strip() or None,
                            observation=observation.strip() or None,
                            is_active=is_active,
                        )
                    )
                    session.commit()
                    st.success("Cliente cadastrado com sucesso!")
                else:
                    st.warning("Informe nome, CPF e e-mail.")
            st.rerun()

    st.markdown("### Lista de clientes")
    if not clientes:
        st.write("Nenhum cliente cadastrado.")
        return

    for item in clientes:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**{item.name}**")
        col2.write(f"CPF: {item.cpf}")
        col3.write(f"Status: {'Ativo' if item.is_active else 'Inativo'}")
        if col4.button("Excluir", key=f"del-client-{item.id}"):
            delete_record(Client, item.id)
            st.rerun()


def render_employees():
    st.title("CRUD de Funcionários")

    with SessionLocal() as session:
        funcionarios = session.query(Employee).order_by(Employee.id.desc()).all()

    selected_id = st.selectbox(
        "Editar funcionário existente",
        [0] + [func.id for func in funcionarios],
        format_func=lambda value: "Novo funcionário" if value == 0 else f"Funcionário {value}",
    )

    current = next((f for f in funcionarios if f.id == selected_id), None) if selected_id else None

    with st.form("form_funcionario"):
        name = st.text_input("Nome", value=current.name if current else "")
        cpf = st.text_input("CPF", value=current.cpf if current else "")
        email = st.text_input("Email", value=current.email if current else "")
        phone = st.text_input("Telefone", value=current.phone if current else "")
        hire_date = st.date_input("Data de contratação", value=current.hire_date if current else date.today())
        role = st.text_input("Função", value=current.role if current else "")
        password = st.text_input("Senha", type="password", value=current.password if current else "")
        is_active = st.checkbox("Ativo", value=current.is_active if current else True)
        submitted = st.form_submit_button("Salvar funcionário")

    if submitted:
        with SessionLocal() as session:
            if selected_id:
                item = session.get(Employee, selected_id)
                if item:
                    item.name = name.strip()
                    item.cpf = cpf.strip()
                    item.email = email.strip()
                    item.phone = phone.strip() or None
                    item.hire_date = hire_date
                    item.role = role.strip() or "Vendedor"
                    item.password = password.strip() or item.password
                    item.is_active = is_active
                    session.commit()
                    st.success("Funcionário atualizado com sucesso!")
            else:
                if name.strip() and cpf.strip() and email.strip() and password.strip():
                    session.add(
                        Employee(
                            name=name.strip(),
                            cpf=cpf.strip(),
                            email=email.strip(),
                            phone=phone.strip() or None,
                            hire_date=hire_date,
                            role=role.strip() or "Vendedor",
                            password=password.strip(),
                            is_active=is_active,
                        )
                    )
                    session.commit()
                    st.success("Funcionário cadastrado com sucesso!")
                else:
                    st.warning("Informe nome, CPF, e-mail e senha.")
            st.rerun()

    st.markdown("### Lista de funcionários")
    if not funcionarios:
        st.write("Nenhum funcionário cadastrado.")
        return

    for item in funcionarios:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**{item.name}**")
        col2.write(f"Função: {item.role}")
        col3.write(f"Status: {'Ativo' if item.is_active else 'Inativo'}")
        if col4.button("Excluir", key=f"del-employee-{item.id}"):
            delete_record(Employee, item.id)
            st.rerun()


def render_suppliers():
    st.title("CRUD de Fornecedores")

    with SessionLocal() as session:
        fornecedores = session.query(Supplier).order_by(Supplier.id.desc()).all()

    selected_id = st.selectbox(
        "Editar fornecedor existente",
        [0] + [fornecedor.id for fornecedor in fornecedores],
        format_func=lambda value: "Novo fornecedor" if value == 0 else f"Fornecedor {value}",
    )

    current = next((f for f in fornecedores if f.id == selected_id), None) if selected_id else None

    with st.form("form_fornecedor"):
        name = st.text_input("Nome ou razão social", value=current.name if current else "")
        document_number = st.text_input("CNPJ ou CPF", value=current.document_number if current else "")
        email = st.text_input("Email", value=current.email if current else "")
        phone = st.text_input("Telefone", value=current.phone if current else "")
        address = st.text_area("Endereço", value=current.address if current else "")
        observation = st.text_area("Observação", value=current.observation if current else "")
        is_active = st.checkbox("Ativo", value=current.is_active if current else True)
        submitted = st.form_submit_button("Salvar fornecedor")

    if submitted:
        with SessionLocal() as session:
            if selected_id:
                item = session.get(Supplier, selected_id)
                if item:
                    item.name = name.strip()
                    item.document_number = document_number.strip()
                    item.email = email.strip() or None
                    item.phone = phone.strip() or None
                    item.address = address.strip() or None
                    item.observation = observation.strip() or None
                    item.is_active = is_active
                    session.commit()
                    st.success("Fornecedor atualizado com sucesso!")
            else:
                if name.strip() and document_number.strip():
                    session.add(
                        Supplier(
                            name=name.strip(),
                            document_number=document_number.strip(),
                            email=email.strip() or None,
                            phone=phone.strip() or None,
                            address=address.strip() or None,
                            observation=observation.strip() or None,
                            is_active=is_active,
                        )
                    )
                    session.commit()
                    st.success("Fornecedor cadastrado com sucesso!")
                else:
                    st.warning("Informe nome e documento do fornecedor.")
            st.rerun()

    st.markdown("### Lista de fornecedores")
    if not fornecedores:
        st.write("Nenhum fornecedor cadastrado.")
        return

    for item in fornecedores:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**{item.name}**")
        col2.write(f"Documento: {item.document_number}")
        col3.write(f"Status: {'Ativo' if item.is_active else 'Inativo'}")
        if col4.button("Excluir", key=f"del-supplier-{item.id}"):
            delete_record(Supplier, item.id)
            st.rerun()


def render_sales():
    st.title("CRUD de Vendas")

    with SessionLocal() as session:
        clientes = session.query(Client).filter(Client.is_active.is_(True)).all()
        funcionarios = session.query(Employee).filter(Employee.is_active.is_(True)).all()
        vendas = session.query(Sale).order_by(Sale.id.desc()).all()

    selected_id = st.selectbox(
        "Editar venda existente",
        [0] + [venda.id for venda in vendas],
        format_func=lambda value: "Nova venda" if value == 0 else f"Venda {value}",
    )

    current = next((v for v in vendas if v.id == selected_id), None) if selected_id else None

    with st.form("form_venda"):
        client_id = st.selectbox(
            "Cliente",
            options=[c.id for c in clientes],
            format_func=lambda value: next((c.name for c in clientes if c.id == value), str(value)),
            index=(next((i for i, c in enumerate(clientes) if current and c.id == current.client_id), 0) if current else 0),
        )
        employee_id = st.selectbox(
            "Funcionário",
            options=[f.id for f in funcionarios],
            format_func=lambda value: next((f.name for f in funcionarios if f.id == value), str(value)),
            index=(next((i for i, f in enumerate(funcionarios) if current and f.id == current.employee_id), 0) if current else 0),
        )
        sale_date = st.date_input("Data da venda", value=current.sale_date.date() if current else date.today())
        payment_method = st.selectbox("Forma de pagamento", ["Pix", "Dinheiro", "Cartão de crédito", "Cartão de débito"], index=(0 if not current else ["Pix", "Dinheiro", "Cartão de crédito", "Cartão de débito"].index(current.payment_method) if current.payment_method in ["Pix", "Dinheiro", "Cartão de crédito", "Cartão de débito"] else 0))
        status = st.selectbox("Status", ["Pendente", "Concluída", "Cancelada"], index=(0 if not current else ["Pendente", "Concluída", "Cancelada"].index(current.status) if current.status in ["Pendente", "Concluída", "Cancelada"] else 0))
        observation = st.text_area("Observação", value=current.observation if current else "")
        total_value = st.number_input("Valor total", min_value=0.0, value=current.total_value if current else 0.0, step=0.5)
        submitted = st.form_submit_button("Salvar venda")

    if submitted:
        with SessionLocal() as session:
            if selected_id:
                item = session.get(Sale, selected_id)
                if item:
                    item.client_id = client_id
                    item.employee_id = employee_id
                    item.sale_date = datetime.combine(sale_date, datetime.now().time())
                    item.total_value = float(total_value)
                    item.payment_method = payment_method
                    item.status = status
                    item.observation = observation.strip() or None
                    session.commit()
                    st.success("Venda atualizada com sucesso!")
            else:
                session.add(
                    Sale(
                        client_id=client_id,
                        employee_id=employee_id,
                        sale_date=datetime.combine(sale_date, datetime.now().time()),
                        total_value=float(total_value),
                        payment_method=payment_method,
                        status=status,
                        observation=observation.strip() or None,
                    )
                )
                session.commit()
                st.success("Venda cadastrada com sucesso!")
            st.rerun()

    st.markdown("### Lista de vendas")
    if not vendas:
        st.write("Nenhuma venda cadastrada.")
        return

    for item in vendas:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**Venda #{item.id}**")
        col2.write(f"Cliente: {item.client.name if item.client else '-'}")
        col3.write(f"Total: R$ {item.total_value:.2f}")
        if col4.button("Excluir", key=f"del-sale-{item.id}"):
            delete_record(Sale, item.id)
            st.rerun()


def render_stock_entries():
    st.title("CRUD de Entradas de Estoque")

    with SessionLocal() as session:
        fornecedores = session.query(Supplier).filter(Supplier.is_active.is_(True)).all()
        funcionarios = session.query(Employee).filter(Employee.is_active.is_(True)).all()
        entradas = session.query(StockEntry).order_by(StockEntry.id.desc()).all()

    selected_id = st.selectbox(
        "Editar entrada existente",
        [0] + [entrada.id for entrada in entradas],
        format_func=lambda value: "Nova entrada" if value == 0 else f"Entrada {value}",
    )

    current = next((e for e in entradas if e.id == selected_id), None) if selected_id else None

    with st.form("form_entrada"):
        supplier_id = st.selectbox(
            "Fornecedor",
            options=[f.id for f in fornecedores],
            format_func=lambda value: next((f.name for f in fornecedores if f.id == value), str(value)),
            index=(next((i for i, f in enumerate(fornecedores) if current and f.id == current.supplier_id), 0) if current else 0),
        )
        employee_id = st.selectbox(
            "Funcionário",
            options=[f.id for f in funcionarios],
            format_func=lambda value: next((f.name for f in funcionarios if f.id == value), str(value)),
            index=(next((i for i, f in enumerate(funcionarios) if current and f.id == current.employee_id), 0) if current else 0),
        )
        received_at = st.date_input("Data de recebimento", value=current.received_at.date() if current else date.today())
        invoice_number = st.text_input("Número da nota fiscal", value=current.invoice_number if current else "")
        total_value = st.number_input("Valor total", min_value=0.0, value=current.total_value if current else 0.0, step=0.5)
        observation = st.text_area("Observação", value=current.observation if current else "")
        confirmed = st.checkbox("Confirmada", value=current.confirmed if current else False)
        submitted = st.form_submit_button("Salvar entrada")

    if submitted:
        with SessionLocal() as session:
            if selected_id:
                item = session.get(StockEntry, selected_id)
                if item:
                    item.supplier_id = supplier_id
                    item.employee_id = employee_id
                    item.received_at = datetime.combine(received_at, datetime.now().time())
                    item.invoice_number = invoice_number.strip()
                    item.total_value = float(total_value)
                    item.observation = observation.strip() or None
                    item.confirmed = confirmed
                    session.commit()
                    st.success("Entrada atualizada com sucesso!")
            else:
                session.add(
                    StockEntry(
                        supplier_id=supplier_id,
                        employee_id=employee_id,
                        received_at=datetime.combine(received_at, datetime.now().time()),
                        invoice_number=invoice_number.strip(),
                        total_value=float(total_value),
                        observation=observation.strip() or None,
                        confirmed=confirmed,
                    )
                )
                session.commit()
                st.success("Entrada cadastrada com sucesso!")
            st.rerun()

    st.markdown("### Lista de entradas")
    if not entradas:
        st.write("Nenhuma entrada cadastrada.")
        return

    for item in entradas:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**Entrada #{item.id}**")
        col2.write(f"Nota: {item.invoice_number}")
        col3.write(f"Status: {'Confirmada' if item.confirmed else 'Pendente'}")
        if col4.button("Excluir", key=f"del-entry-{item.id}"):
            delete_record(StockEntry, item.id)
            st.rerun()


navigation = st.sidebar.radio(
    "Navegação",
    [
        "Resumo",
        "Categorias",
        "Marcas",
        "Roupas",
        "Variações",
        "Clientes",
        "Funcionários",
        "Fornecedores",
        "Vendas",
        "Entradas do Estoque",
    ],
)

if navigation == "Resumo":
    render_summary()
elif navigation == "Categorias":
    render_categories()
elif navigation == "Marcas":
    render_brands()
elif navigation == "Roupas":
    render_clothes()
elif navigation == "Variações":
    render_variations()
elif navigation == "Clientes":
    render_clients()
elif navigation == "Funcionários":
    render_employees()
elif navigation == "Fornecedores":
    render_suppliers()
elif navigation == "Vendas":
    render_sales()
else:
    render_stock_entries()
