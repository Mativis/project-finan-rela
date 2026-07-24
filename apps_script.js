// ─── SETUP INICIAL ────────────────────────────────────────────────────────────
function setupBancoDados() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  criarAba(ss, "Categorias", ["ID", "Nome", "Tipo"]);
  [
    ["1","Salario","Receita"],["2","Freelance","Receita"],
    ["3","Investimentos","Receita"],["4","Outros","Receita"],
    ["5","Moradia","Despesa"],["6","Alimentacao","Despesa"],
    ["7","Transporte","Despesa"],["8","Saude","Despesa"],
    ["9","Educacao","Despesa"],["10","Lazer","Despesa"],
    ["11","Vestuario","Despesa"],["12","Contas Fixas","Despesa"],
    ["13","Assinaturas","Despesa"],["14","Presentes","Despesa"],
    ["15","Outros","Despesa"]
  ].forEach(function(c){ ss.getSheetByName("Categorias").appendRow(c); });

  criarAba(ss, "Transacoes", ["ID","Data","Tipo","Categoria","Descricao","Valor","Parcelas","Responsavel"]);
  criarAba(ss, "Metas", ["ID","Nome","ValorAlvo","ValorAtual","Prazo"]);
  criarAba(ss, "Config", ["Chave","Valor"]);
  ss.getSheetByName("Config").appendRow(["Moeda","BRL"]);

  try { ss.deleteSheet(ss.getSheetByName("Sheet1")); } catch(e){}

  // Deploy manual
  var url = ScriptApp.getService().getUrl();
  if (!url) url = "Publicar > Implantar como aplicativo da web";

  SpreadsheetApp.getUi().alert(
    "Setup concluido!\n\n" +
    "Abas: Categorias, Transacoes, Metas, Config\n\n" +
    "Agora va em:\n" +
    "Implantar > Nova implantacao > Aplicativo da web\n" +
    "Executar como: Eu, Acesso: Qualquer pessoa\n\n" +
    "Copie a URL gerada e cole no .env:\n" +
    "API_URL=SUA_URL_AQUI"
  );
}

function criarAba(ss, nome, cabecalho) {
  var s = ss.getSheetByName(nome);
  if (s) ss.deleteSheet(s);
  s = ss.insertSheet(nome);
  s.appendRow(cabecalho);
  var r = s.getRange(1, 1, 1, cabecalho.length);
  r.setFontWeight("bold").setBackground("#4a86c8").setFontColor("#ffffff");
  s.setFrozenRows(1);
  return s;
}

// ─── WEB APP API ──────────────────────────────────────────────────────────────
function doGet(e) {
  var acao = e.parameter.acao || "";
  var aba = e.parameter.aba || "";

  if (!aba) return resposta(400, "Parametro 'aba' obrigatorio");

  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(aba);
    if (!sheet) return resposta(404, "Aba '" + aba + "' nao encontrada");

    if (acao == "ler") {
      var dados = sheet.getDataRange().getValues();
      if (dados.length < 2) return resposta(200, []);
      var cabecalho = dados[0];
      var linhas = [];
      for (var i = 1; i < dados.length; i++) {
        var obj = {};
        for (var j = 0; j < cabecalho.length; j++) {
          obj[cabecalho[j]] = dados[i][j];
        }
        linhas.push(obj);
      }
      return resposta(200, linhas);
    }

    if (acao == "proximo_id") {
      var dados = sheet.getDataRange().getValues();
      if (dados.length < 2) return resposta(200, {proximo_id: "1"});
      var ids = [];
      for (var i = 1; i < dados.length; i++) {
        ids.push(parseInt(dados[i][0]) || 0);
      }
      return resposta(200, {proximo_id: String(Math.max.apply(null, ids) + 1)});
    }

    return resposta(400, "Acao invalida");
  } catch(err) {
    return resposta(500, "Erro: " + err.message);
  }
}

function doPost(e) {
  try {
    var dados = JSON.parse(e.postData.contents);
    var aba = dados.aba || "";
    var valores = dados.valores || [];

    if (!aba) return resposta(400, "Parametro 'aba' obrigatorio");
    if (!valores.length) return resposta(400, "Parametro 'valores' obrigatorio");

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(aba);
    if (!sheet) return resposta(404, "Aba '" + aba + "' nao encontrada");

    sheet.appendRow(valores);
    return resposta(200, {status: "ok", mensagem: "Registro adicionado"});
  } catch(err) {
    return resposta(500, "Erro: " + err.message);
  }
}

function doDelete(e) {
  try {
    var aba = e.parameter.aba || "";
    var id = e.parameter.id || "";

    if (!aba || !id) return resposta(400, "Parametros 'aba' e 'id' obrigatorios");

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(aba);
    if (!sheet) return resposta(404, "Aba nao encontrada");

    var dados = sheet.getDataRange().getValues();
    for (var i = 1; i < dados.length; i++) {
      if (String(dados[i][0]).trim() == id.trim()) {
        sheet.deleteRow(i + 1);
        return resposta(200, {status: "ok", mensagem: "Registro " + id + " excluido"});
      }
    }
    return resposta(404, "ID nao encontrado");
  } catch(err) {
    return resposta(500, "Erro: " + err.message);
  }
}

function resposta(codigo, conteudo) {
  return ContentService
    .createTextOutput(JSON.stringify(conteudo))
    .setMimeType(ContentService.MimeType.JSON);
}

function onOpen() {
  SpreadsheetApp.getUi().createMenu("Financeiro")
    .addItem("Setup Banco de Dados", "setupBancoDados")
    .addToUi();
}