document.addEventListener("DOMContentLoaded", function () {
    const tabela = document.getElementById("servicos-tabela");
    const paginacao = document.getElementById("paginacao");
    const filtroForm = document.getElementById("filtro-servicos");

    function mostrarLoading() {
        tabela.innerHTML = `
            <div class="d-flex justify-content-center my-4">
                <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
            </div>
        `;
    }

    function carregarServicos(pagina = 1) {
        mostrarLoading();
        const formData = new FormData(filtroForm);
        const params = new URLSearchParams(formData);
        params.append('page', pagina);

        fetch(`/auth/admin/servicos_json/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                // Monta tabela com wrapper responsivo
                let html = `
                    <div class="table-responsive">
                        <table class="table table-bordered table-hover align-middle">
                            <thead class="table-dark">
                                <tr>
                                    <th>Nome</th>
                                    <th>Protocolo</th>
                                    <th>Categorias</th>
                                    <th>Status</th>
                                    <th>Data</th>
                                    <th>Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                `;
                data.servicos.forEach(s => {
                    html += `
                        <tr>
                            <td>${s.nome}</td>
                            <td>${s.protocolo}</td>
                            <td>${s.categorias.length > 0 
                                ? s.categorias.map(c => `<span class="badge bg-success me-1">${c}</span>`).join(" ") 
                                : `<span class="text-muted">Sem categorias</span>`}
                            </td>
                            <td><span class="badge bg-success">${s.status}</span></td>
                            <td>${s.data_criacao}</td>
                            <td>
                                <a href="/auth/servico/${s.id}/" class="btn btn-sm btn-primary me-1">Detalhes</a>
                                
                            </td>
                        </tr>
                    `;
                });
                html += "</tbody></table></div>";
                tabela.innerHTML = html;

                // ---- PAGINAÇÃO MELHORADA ----
                let pagHtml = `<ul class="pagination justify-content-center">`;

                // Botão "Anterior"
                if (data.current_page > 1) {
                    pagHtml += `
                        <li class="page-item">
                            <a href="#" class="page-link" data-pagina="${data.current_page - 1}">Anterior</a>
                        </li>`;
                } else {
                    pagHtml += `<li class="page-item disabled"><span class="page-link">Anterior</span></li>`;
                }

                // Páginas (2 antes e 2 depois da atual)
                let start = Math.max(1, data.current_page - 2);
                let end = Math.min(data.num_pages, data.current_page + 2);

                if (start > 1) {
                    pagHtml += `<li class="page-item"><a href="#" class="page-link" data-pagina="1">1</a></li>`;
                    if (start > 2) {
                        pagHtml += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
                    }
                }

                for (let i = start; i <= end; i++) {
                    pagHtml += `
                        <li class="page-item ${i === data.current_page ? "active" : ""}">
                            <a href="#" class="page-link" data-pagina="${i}">${i}</a>
                        </li>`;
                }

                if (end < data.num_pages) {
                    if (end < data.num_pages - 1) {
                        pagHtml += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
                    }
                    pagHtml += `<li class="page-item"><a href="#" class="page-link" data-pagina="${data.num_pages}">${data.num_pages}</a></li>`;
                }

                // Botão "Próximo"
                if (data.current_page < data.num_pages) {
                    pagHtml += `
                        <li class="page-item">
                            <a href="#" class="page-link" data-pagina="${data.current_page + 1}">Próximo</a>
                        </li>`;
                } else {
                    pagHtml += `<li class="page-item disabled"><span class="page-link">Próximo</span></li>`;
                }

                pagHtml += "</ul>";
                paginacao.innerHTML = pagHtml;

                // Eventos clique paginação
                document.querySelectorAll("#paginacao a").forEach(link => {
                    link.addEventListener("click", e => {
                        e.preventDefault();
                        carregarServicos(parseInt(link.dataset.pagina));
                    });
                });
            })
            .catch(() => {
                tabela.innerHTML = `
                    <div class="alert alert-danger text-center mt-3">
                        Erro ao carregar os serviços. Tente novamente.
                    </div>
                `;
            });
    }

    // Evento de submit no formulário de filtros
    filtroForm.addEventListener("submit", function (e) {
        e.preventDefault();
        carregarServicos(1);
    });

    carregarServicos();
});

// Select2 para categorias
$(document).ready(function () {
    $("#categorias").select2({
        placeholder: "Selecione categorias",
        allowClear: true,
        width: "100%"
    });
});
