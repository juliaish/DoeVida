  var map = L.map('map').setView([-23.5505, -46.6333], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  var rotaAnterior = null;
  var marcador;
  var destinoSelecionado = null;

  const apiKey = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImIwNGZlNTZmZDI0NTRjZGE4OGVhOTgyOGNiNDYyMjMwIiwiaCI6Im11cm11cjY0In0=';

const locais = {
  "Banco de Sangue de São Paulo": {
    lat: -23.574914618283813,
    lng: -46.64735956651362,
    descricao: "R. Dr. Tomás Carvalhal, 711 - Paraíso, São Paulo - SP, 04006-002"
  },
  "Hemocentro da Santa Casa de São Paulo": {
    lat: -23.543788971762826,
    lng: -46.6499739673451,
    descricao: "R. Marquês de Itu, 579 - Vila Buarque, São Paulo - SP, 01223-001"
  },
  "Hemocentro HSP Unifesp": {
    lat: -23.595216546102392,
    lng: -46.64477181613007,
    descricao: "R. Dr. Diogo de Faria, 824 - Vila Clementino, São Paulo - SP, 04037-002"
  },
  "Hemocentro São Lucas": {
    lat: -23.652441527488598,
    lng: -46.710166624299525,
    descricao: "Granja Julieta - R. Amador Bueno, 229 - Piso 1 - Santo Amaro, São Paulo - SP, 04752-005"
  },
  "Hospital A.C Camargo": {
    lat: -23.563307337388668,
    lng: -46.636609326988335,
    descricao: "R. Taguá, 440 - Liberdade, São Paulo - SP, 01508-010"
  },
  "Hospital do Coração": {
    lat: -23.5728570247739,
    lng: -46.643683837016226,
    descricao: "R. Des. Eliseu Guilherme, 147 - Paraíso, São Paulo - SP, 04004-030"
  },
  "Hospital Israelita Albert Einstein": {
    lat: -23.59994734606646,
    lng: -46.71492919193734,
    descricao: "Av. Albert Einstein, 627/701 - Morumbi, São Paulo - SP, 05652-900"
  },
  "Hospital Leforte": {
    lat: -23.584295901397915,
    lng: -46.71764773201868,
    descricao: "Rua dos Três Irmãos, 121 - Morumbi, São Paulo - SP, 05615-190"
  },
  "Hospital Professor Edmundo Vasconcelos": {
    lat: -23.595646809599067,
    lng: -46.65141330693846,
    descricao: "R. Borges Lagoa, 1450 - Vila Clementino, São Paulo - SP, 04038-905"
  },
  "Hospital Santa Catarina": {
    lat: -23.566163182835588,
    lng: -46.64540684129627,
    descricao: "Av. Paulista, 200 - Bela Vista, São Paulo - SP, 01310-000"
  },
  "Hospital Santa Paula": {
    lat: -23.605626302361824,
    lng: -46.67573383538347,
    descricao: "Av. Santo Amaro, 2468 - Brooklin, São Paulo - SP, 04556-100"
  },
  "Hospital Sírio Libanês": {
    lat: -23.55694731449014,
    lng: -46.653678843662355,
    descricao: "Rua Dona Adma Jafet, 115 - Bela Vista, São Paulo - SP, 01308-050"
  },
  "Instituto HOC de Hemoterapia": {
    lat: -23.568386335325894,
    lng: -46.643276273801476,
    descricao: "R. João Julião, 331 - Bela Vista, São Paulo - SP, 01323-020"
  },
  "Pró Sangue": {
    lat: -23.551514547227836,
    lng: -46.66710931438585,
    descricao: "Av. Dr. Enéas Carvalho de Aguiar, 155 - 1° andar - Cerqueira César, São Paulo - SP, 05403-000"
  },
  "Pulsa São Paulo Banco de Sangue Paulista": {
    lat: -23.65425498312573,
    lng: -46.70495818653628,
    descricao: "R. Iguatinga, 382 - Santo Amaro, São Paulo - SP, 04744-040"
  }
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
