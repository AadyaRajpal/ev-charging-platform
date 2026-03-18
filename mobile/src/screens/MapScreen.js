import { useState, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, SafeAreaView, ActivityIndicator, Alert, TextInput } from 'react-native';
import MapView, { Marker, Callout } from 'react-native-maps';
import * as Location from 'expo-location';
import { Ionicons } from '@expo/vector-icons';
import { fetchStations } from '../api/stations';

const C = {
  bg: '#0a0f0d', surface: '#111812', surface2: '#172019',
  border: '#1e2e21', accent: '#00ff87', text: '#e8f5ec',
  muted: '#6b8c72', red: '#ff4d6a', yellow: '#ffd166',
};

export default function MapScreen({ navigation }) {
  const mapRef = useRef(null);
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [radius, setRadius] = useState('10');
  const [region, setRegion] = useState({
    latitude: 12.9716, longitude: 77.5946,
    latitudeDelta: 0.2, longitudeDelta: 0.2,
  });

  function statusColor(status) {
    if (status === 'Available') return C.accent;
    if (status === 'Unavailable') return C.red;
    return C.yellow;
  }

  async function searchHere() {
    setLoading(true);
    try {
      const results = await fetchStations({
        lat: region.latitude, lng: region.longitude,
        radius: parseInt(radius) || 10,
      });
      setStations(results);
    } catch {
      Alert.alert('Error', 'Could not reach backend.');
    } finally {
      setLoading(false);
    }
  }

  async function goToMyLocation() {
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') return;
    const loc = await Location.getCurrentPositionAsync({});
    const newRegion = {
      latitude: loc.coords.latitude,
      longitude: loc.coords.longitude,
      latitudeDelta: 0.1, longitudeDelta: 0.1,
    };
    setRegion(newRegion);
    mapRef.current?.animateToRegion(newRegion, 800);
  }

  return (
    <SafeAreaView style={s.safe}>
      <View style={s.header}>
        <Text style={s.logo}><Text style={s.logoGreen}>EV</Text>Find</Text>
        <View style={s.headerRight}>
          <Text style={s.label}>RADIUS</Text>
          <TextInput
            style={s.radiusInput} value={radius}
            onChangeText={setRadius} keyboardType="numeric"
          />
        </View>
      </View>

      <View style={s.mapContainer}>
        <MapView
          ref={mapRef}
          style={s.map}
          initialRegion={region}
          onRegionChangeComplete={setRegion}
          userInterfaceStyle="dark"
        >
          {stations.map(s => (
            s.lat && s.lng ? (
              <Marker
                key={s.id}
                coordinate={{ latitude: s.lat, longitude: s.lng }}
                pinColor={statusColor(s.status)}
              >
                <Callout onPress={() => navigation.navigate('StationDetail', { station: s })}>
                  <View style={callout.box}>
                    <Text style={callout.name}>{s.name}</Text>
                    <Text style={callout.detail}>{s.status} · {s.num_points} points</Text>
                    <Text style={callout.tap}>Tap for details →</Text>
                  </View>
                </Callout>
              </Marker>
            ) : null
          ))}
        </MapView>

        {/* FABs */}
        <TouchableOpacity style={[s.fab, s.fabLocate]} onPress={goToMyLocation}>
          <Ionicons name="locate" size={20} color={C.accent} />
        </TouchableOpacity>

        <TouchableOpacity style={[s.fab, s.fabSearch]} onPress={searchHere} disabled={loading}>
          {loading
            ? <ActivityIndicator size="small" color={C.bg} />
            : <Text style={s.fabText}>Search here</Text>
          }
        </TouchableOpacity>

        {stations.length > 0 && (
          <View style={s.countBadge}>
            <Text style={s.countText}>{stations.length} stations</Text>
          </View>
        )}
      </View>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  safe: { flex: 1, backgroundColor: C.bg },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 16, backgroundColor: C.surface, borderBottomWidth: 1, borderBottomColor: C.border },
  logo: { fontSize: 20, fontWeight: '800', color: C.text },
  logoGreen: { color: C.accent },
  headerRight: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  label: { fontSize: 10, color: C.muted, letterSpacing: 1 },
  radiusInput: { backgroundColor: C.surface2, borderWidth: 1, borderColor: C.border, color: C.text, padding: 6, borderRadius: 6, width: 50, fontSize: 13, textAlign: 'center' },
  mapContainer: { flex: 1, position: 'relative' },
  map: { flex: 1 },
  fab: { position: 'absolute', borderRadius: 25, elevation: 4, shadowColor: '#000', shadowOpacity: 0.3, shadowRadius: 4 },
  fabLocate: { bottom: 80, right: 16, backgroundColor: C.surface, borderWidth: 1, borderColor: C.border, width: 44, height: 44, alignItems: 'center', justifyContent: 'center' },
  fabSearch: { bottom: 24, alignSelf: 'center', left: '50%', marginLeft: -60, backgroundColor: C.accent, paddingHorizontal: 20, paddingVertical: 12, width: 140, alignItems: 'center' },
  fabText: { color: C.bg, fontWeight: '700', fontSize: 13 },
  countBadge: { position: 'absolute', top: 12, alignSelf: 'center', left: '50%', marginLeft: -45, backgroundColor: C.surface, borderWidth: 1, borderColor: C.border, paddingHorizontal: 12, paddingVertical: 5, borderRadius: 20 },
  countText: { color: C.accent, fontSize: 12, fontWeight: '600' },
});

const callout = StyleSheet.create({
  box: { width: 180, padding: 8 },
  name: { fontWeight: '700', fontSize: 13, marginBottom: 2 },
  detail: { fontSize: 12, color: '#555', marginBottom: 4 },
  tap: { fontSize: 11, color: '#888' },
});
