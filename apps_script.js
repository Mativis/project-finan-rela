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

  var url = ScriptApp.getService().getUrl();
  if (!url) url = "Apos implantar como Web App";

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
  r.setFontWeight("bold").setBackground("#4f46e5").setFontColor("#ffffff");
  s.setFrozenRows(1);
  return s;
}

function doGet(e) {
  var acao = e.parameter.acao || e.parameter.action || "";
  var aba = e.parameter.aba || e.parameter.sheet || "";
  var callback = e.parameter.callback || "";

  if (!aba) return resposta(400, {erro: "Parametro 'aba' obrigatorio"}, callback);

  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(aba);
    if (!sheet) return resposta(404, {erro: "Aba '" + aba + "' nao encontrada"}, callback);

    if (acao == "ler" || acao == "read") {
      var dados = sheet.getDataRange().getValues();
      if (dados.length < 2) return resposta(200, [], callback);
      var cabecalho = dados[0];
      var linhas = [];
      for (var i = 1; i < dados.length; i++) {
        var obj = {};
        for (var j = 0; j < cabecalho.length; j++) {
          obj[cabecalho[j]] = dados[i][j];
        }
        linhas.push(obj);
      }
      return resposta(200, linhas, callback);
    }

    if (acao == "proximo_id" || acao == "next_id") {
      var dados = sheet.getDataRange().getValues();
      if (dados.length < 2) return resposta(200, {proximo_id: "1"}, callback);
      var ids = [];
      for (var i = 1; i < dados.length; i++) {
        ids.push(parseInt(dados[i][0]) || 0);
      }
      return resposta(200, {proximo_id: String(Math.max.apply(null, ids) + 1)}, callback);
    }

    if (acao == "ping" || acao == "health") {
      return resposta(200, {status: "ok", mensagem: "API funcionando", abas: ss.getSheets().map(function(s){ return s.getName(); })}, callback);
    }

    return resposta(400, {erro: "Acao invalida: " + acao}, callback);
  } catch(err) {
    return resposta(500, {erro: "Erro interno: " + err.message}, callback);
  }
}

function doPost(e) {
  var callback = "";
  try {
    var raw = e.postData.contents;
    var dados = JSON.parse(raw);
    var aba = dados.aba || dados.sheet || "";
    var valores = dados.valores || dados.values || [];
    callback = dados.callback || "";

    if (!aba) return resposta(400, {erro: "Parametro 'aba' obrigatorio"}, callback);
    if (!valores || !valores.length) return resposta(400, {erro: "Parametro 'valores' obrigatorio"}, callback);

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(aba);
    if (!sheet) return resposta(404, {erro: "Aba '" + aba + "' nao encontrada"}, callback);

    sheet.appendRow(valores);
    return resposta(200, {status: "ok", mensagem: "Registro adicionado"}, callback);
  } catch(err) {
    return resposta(500, {erro: "Erro: " + err.message}, callback);
  }
}

function doDelete(e) {
  var callback = e.parameter.callback || "";
  try {
    var aba = e.parameter.aba || e.parameter.sheet || "";
    var id = e.parameter.id || "";

    if (!aba || !id) return resposta(400, {erro: "Parametros 'aba' e 'id' obrigatorios"}, callback);

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(aba);
    if (!sheet) return resposta(404, {erro: "Aba nao encontrada"}, callback);

    var dados = sheet.getDataRange().getValues();
    for (var i = 1; i < dados.length; i++) {
      if (String(dados[i][0]).trim() == id.trim()) {
        sheet.deleteRow(i + 1);
        return resposta(200, {status: "ok", mensagem: "Registro " + id + " excluido"}, callback);
      }
    }
    return resposta(404, {erro: "ID nao encontrado"}, callback);
  } catch(err) {
    return resposta(500, {erro: "Erro: " + err.message}, callback);
  }
}

function doPut(e) {
  var callback = "";
  try {
    var raw = e.postData.contents;
    var dados = JSON.parse(raw);
    var aba = dados.aba || dados.sheet || "";
    var id = dados.id || "";
    var valores = dados.valores || dados.values || [];
    callback = dados.callback || "";

    if (!aba || !id) return resposta(400, {erro: "Parametros 'aba' e 'id' obrigatorios"}, callback);
    if (!valores || !valores.length) return resposta(400, {erro: "Parametro 'valores' obrigatorio"}, callback);

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(aba);
    if (!sheet) return resposta(404, {erro: "Aba nao encontrada"}, callback);

    var data = sheet.getDataRange().getValues();
    var cabecalho = data[0];
    for (var i = 1; i < data.length; i++) {
      if (String(data[i][0]).trim() == id.trim()) {
        var range = sheet.getRange(i + 1, 1, 1, cabecalho.length);
        range.setValues([valores]);
        return resposta(200, {status: "ok", mensagem: "Registro " + id + " atualizado"}, callback);
      }
    }
    return resposta(404, {erro: "ID nao encontrado"}, callback);
  } catch(err) {
    return resposta(500, {erro: "Erro: " + err.message}, callback);
  }
}

function resposta(httpCode, conteudo, callback) {
  if (typeof conteudo !== "object" || conteudo === null) conteudo = {};
  conteudo._httpCode = httpCode;
  var json = JSON.stringify(conteudo);
  var output = ContentService.createTextOutput(json).setMimeType(ContentService.MimeType.JSON);
  if (callback) {
    output = ContentService.createTextOutput(callback + "(" + json + ")").setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return output;
}

function onOpen() {
  SpreadsheetApp.getUi().createMenu("Financeiro")
    .addItem("Setup Banco de Dados", "setupBancoDados")
    .addToUi();
}
