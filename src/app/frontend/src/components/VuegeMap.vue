<template>
  <div class="vuege-map">
    <div ref="mapContainer" class="map-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Props
interface Props {
  center?: [number, number]
  zoom?: number
  markers?: Array<{
    position: [number, number]
    title: string
    description?: string
  }>
  polygons?: Array<{
    coordinates: [number, number][]
    color?: string
    title?: string
  }>
}

const props = withDefaults(defineProps<Props>(), {
  center: () => [55.7558, 37.6176], // Москва по умолчанию
  zoom: 10,
  markers: () => [],
  polygons: () => []
})

// Refs
const mapContainer = ref<HTMLElement>()
let map: L.Map | null = null
let markers: L.Marker[] = []
let polygons: L.Polygon[] = []

// Инициализация карты
const initMap = () => {
  if (!mapContainer.value) return

  // Создание карты
  map = L.map(mapContainer.value).setView(props.center, props.zoom)

  // Добавление тайлов OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map)

  // Добавление маркеров
  addMarkers()
  
  // Добавление полигонов
  addPolygons()
}

// Добавление маркеров
const addMarkers = () => {
  if (!map) return

  // Очистка существующих маркеров
  markers.forEach(marker => map?.removeLayer(marker))
  markers = []

  // Добавление новых маркеров
  props.markers.forEach(markerData => {
    const marker = L.marker(markerData.position)
      .addTo(map!)
      .bindPopup(`
        <div>
          <h4>${markerData.title}</h4>
          ${markerData.description ? `<p>${markerData.description}</p>` : ''}
        </div>
      `)
    
    markers.push(marker)
  })
}

// Добавление полигонов
const addPolygons = () => {
  if (!map) return

  // Очистка существующих полигонов
  polygons.forEach(polygon => map?.removeLayer(polygon))
  polygons = []

  // Добавление новых полигонов
  props.polygons.forEach(polygonData => {
    const polygon = L.polygon(polygonData.coordinates, {
      color: polygonData.color || '#3388ff',
      fillColor: polygonData.color || '#3388ff',
      fillOpacity: 0.2,
      weight: 2
    })
      .addTo(map!)
    
    if (polygonData.title) {
      polygon.bindPopup(`<div><h4>${polygonData.title}</h4></div>`)
    }
    
    polygons.push(polygon)
  })
}

// Обновление карты при изменении props
watch(() => props.center, (newCenter) => {
  if (map && newCenter) {
    map.setView(newCenter, props.zoom)
  }
}, { deep: true })

watch(() => props.zoom, (newZoom) => {
  if (map) {
    map.setZoom(newZoom)
  }
})

watch(() => props.markers, () => {
  addMarkers()
}, { deep: true })

watch(() => props.polygons, () => {
  addPolygons()
}, { deep: true })

// Lifecycle
onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
})

// Expose methods
defineExpose({
  getMap: () => map,
  addMarker: (position: [number, number], title: string, description?: string) => {
    if (!map) return
    
    const marker = L.marker(position)
      .addTo(map)
      .bindPopup(`
        <div>
          <h4>${title}</h4>
          ${description ? `<p>${description}</p>` : ''}
        </div>
      `)
    
    markers.push(marker)
    return marker
  },
  addPolygon: (coordinates: [number, number][], color?: string, title?: string) => {
    if (!map) return
    
    const polygon = L.polygon(coordinates, {
      color: color || '#3388ff',
      fillColor: color || '#3388ff',
      fillOpacity: 0.2,
      weight: 2
    })
      .addTo(map)
    
    if (title) {
      polygon.bindPopup(`<div><h4>${title}</h4></div>`)
    }
    
    polygons.push(polygon)
    return polygon
  },
  clearMarkers: () => {
    markers.forEach(marker => map?.removeLayer(marker))
    markers = []
  },
  clearPolygons: () => {
    polygons.forEach(polygon => map?.removeLayer(polygon))
    polygons = []
  }
})
</script>

<style scoped>
.vuege-map {
  width: 100%;
  height: 100%;
}

.map-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style>