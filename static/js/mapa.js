  var map = L.map('map').setView([-23.5505, -46.6333], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  var rotaAnterior = null;
  var marcador;
  var destinoSelecionado = null;

  const apiKey = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImIwNGZlNTZmZDI0NTRjZGE4OGVhOTgyOGNiNDYyMjMwIiwiaCI6Im11cm11cjY0In0=';

  const locais = {
    "Hemocentro São Lucas": { lat: -23.652441527488598, lng: -46.710166624299525, descricao: "Centro especializado em coleta e distribuição de sangue..." },
    "Hemocentro HSP Unifesp": { lat: -23.595216546102392, lng: -46.64477181613007, descricao: "Unidade vinculada à Unifesp..." },
    "Hospital Leforte": { lat: -23.584295901397915, lng: -46.71764773201868, descricao: "Hospital com infraestrutura completa..." },
    "Banco de Sangue de São Paulo": { lat: -23.574914618283813, lng: -46.64735956651362, descricao: "Instituição dedicada à coleta..." },
    "Instituto HOC de Hemoterapia": { lat: -23.568386335325894, lng: -46.643276273801476, descricao: "Referência em hemoterapia..." },
    "Pulsa São Paulo Banco de Sangue Paulista": { lat: -23.65425498312573, lng: -46.70495818653628, descricao: "Banco de sangue com foco em inovação..." },
    "Pró Sangue": { lat: -23.551514547227836, lng: -46.66710931438585, descricao: "Fundação pública que promove campanhas..." },
    "Hospital Santa Catarina": { lat: -23.566163182835588, lng: -46.64540684129627, descricao: "Hospital tradicional com atendimento humanizado..." },
    "Hospital Sírio Libanês": { lat: -23.55694731449014, lng: -46.653678843662355, descricao: "Um dos hospitais mais renomados do Brasil..." },
    "Hemocentro da Santa Casa de São Paulo": { lat: -23.543788971762826, lng: -46.6499739673451, descricao: "Hemocentro vinculado à Santa Casa..." },
    "Hospital A.C Camargo": { lat: -23.561865774224916, lng: -46.63071314895875, descricao: "Referência nacional em oncologia..." },
    "Hospital Israelita Albert Einstein": { lat: -23.59994734606646, lng: -46.71492919193734, descricao: "Hospital de excelência com foco em tecnologia..." },
    "Hospital do Coração": { lat: -23.5728570247739, lng: -46.643683837016226, descricao: "Especializado em cardiologia..." },
    "Hospital Professor Edmundo Vasconcelos": { lat: -23.595646809599067, lng: -46.65141330693846, descricao: "Hospital geral com atendimento humanizado..." },
    "Hospital Santa Paula": { lat: -23.605626302361824, lng: -46.67573383538347, descricao: "Hospital moderno com diversas especialidades..." }
  };

  function mostrarLugar(nome) {
    const lugar = locais[nome];
    if (!lugar) return;

    destinoSelecionado = lugar;

    document.getElementById('info-lugar').innerHTML = `<h3>${nome}</h3><p>${lugar.descricao}</p>`;

    //Estiliza a div com borda.
    document.getElementById('info-lugar').style = "  border: 2px solid #a2272c;  border-radius: 8px; padding: 9px 10px; " 

    map.setView([lugar.lat, lugar.lng], 15);
    if (marcador) map.removeLayer(marcador);
    marcador = L.marker([lugar.lat, lugar.lng]).addTo(map).bindPopup(nome).openPopup();
  }

async function buscarCoordenadas() {
  const endereco = document.getElementById('endereco-partida').value;
  if (!endereco || !destinoSelecionado) {
    alert("Digite o endereço e selecione um local da lista.");
    return;
  }

  try {
    // restringido a buscar somente em São Paulo, Brasil
    const textoBusca = `${endereco}, São Paulo`;
    const url = `https://api.openrouteservice.org/geocode/search?api_key=${apiKey}&text=${encodeURIComponent(textoBusca)}&boundary.country=BR`;

    const response = await fetch(url);
    const data = await response.json();
    console.log("Geocodificação:", data);

    if (data.features.length > 0) {
      const [lngInicio, latInicio] = data.features[0].geometry.coordinates;
      desenharRota(latInicio, lngInicio, destinoSelecionado.lat, destinoSelecionado.lng);
    } else {
      alert("Endereço não encontrado dentro do estado de São Paulo.");
    }
  } catch (error) {
    console.error("Erro ao buscar coordenadas:", error);
    alert("Não foi possível buscar o endereço. Verifique a conexão ou tente novamente.");
  }
}

 async function desenharRota(latInicio, lngInicio, latDestino, lngDestino) {
  try {
    const url = 'https://api.openrouteservice.org/v2/directions/driving-car/geojson';

    const body = {
      coordinates: [
        [lngInicio, latInicio],
        [lngDestino, latDestino]
      ]
    };

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    if (rotaAnterior) {
      map.removeLayer(rotaAnterior);
    }

    rotaAnterior = L.geoJSON(data, {
      style: { color: 'blue', weight: 4 }
    }).addTo(map);
  } catch (error) {
    console.error("Erro ao desenhar rota:", error);
    alert("Não foi possível calcular a rota.");
  }
}
