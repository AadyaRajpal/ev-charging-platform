import { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, FlatList,
  StyleSheet, ActivityIndicator, SafeAreaView, Alert
} from 'react-native';
import * as Location from 'expo-location';
import { Ionicons } from '@expo/vector-icons';
import { fetchStations } from '../api/stations';

const C = {
  bg: '#0a0f0d', surface: '#111812', surface2: '#172019',
  border: '#1e2e21', accent: '#00ff87', accentDim: '#00c96a',
  text: '#e8f5ec', muted: '#6b8c72', red: '#ff4d6a', yellow: '#ffd166',
};

export default function HomeScreen({ navigation }) {
  const [lat, setLat] = useState('12.9716');
  const [lng, setLng] = useState('77.5946');
  const [radius, setRadius] = useState('10');
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function useMyLocation() {
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission denied', 'Allow location access to use this feature.');
      return;
    }
    const loc = await Location.getCurrentPositionAsync({});
    setLat(loc.coords.latitude.toFixed(5));
    setLng(loc.coords.longitude.toFixed(5));
  }

  async function search() {
    if (!lat || !lng) return Alert.alert('Missing', 'Enter latitude and longitude.');
    setLoading(true);
    setSearched(true);
    try {
      const results = await fetchStations({ lat: parseFloat(lat), lng: parseFloat(lng), radius: parseInt(radius) });
      setStations(results);
    } catch (e) {
      Alert.alert('Error', 'Could not reach backend. Make sure FastAPI is running.');
    } finally {
      setLoading(false);
    }
  }

  function statusColor(status) {
    if (status === 'Available') return C.accent;
    if (status === 'Unavailable') return C.red;
    return C.yellow;
  }

  return (
    <SafeAreaView style={s.safe}>
      {/* Header */}
      <View style={s.header}>
        <Text style={s.logo}><Text style={s.logoGreen}>EV</Text>Find</Text>
      </View>

      {/* Search Panel */}
      <View style={s.panel}>
        <View style={s.row}>
          <View style={s.inputGroup}>
            <Text style={s.label}>LATITUDE</Text>
            <TextInput style={s.input} value={lat} onChangeText={setLat} keyboardType="numeric" placeholderTextColor={C.muted} />
          </View>
          <View style={s.inputGroup}>
            <Text style={s.label}>LONGITUDE</Text>
            <TextInput style={s.input} value={lng} onChangeText={setLng} keyboardType="numeric" placeholderTextColor={C.muted} />
          </View>
        </View>
        <View style={s.row}>
          <View style={s.inputGroup}>
            <Text style={s.label}>RADIUS (KM)</Text>
            <TextInput style={s.input} value={radius} onChangeText={setRadius} keyboardType="numeric" placeholderTextColor={C.muted} />
          </View>
          <TouchableOpacity style={s.locBtn} onPress={useMyLocation}>
            <Ionicons name="locate" size={16} color={C.accent} />
            <Text style={s.locBtnText}> My Location</Text>
          </TouchableOpacity>
        </View>
        <TouchableOpacity style={s.searchBtn} onPress={search} disabled={loading}>
          {loading
            ? <ActivityIndicator color={C.bg} />
            : <Text style={s.searchBtnText}>Search Stations</Text>
          }
        </TouchableOpacity>
      </View>

      {/* Results */}
      {!searched ? (
        <View style={s.emptyState}>
          <Text style={s.emptyIcon}>⚡</Text>
          <Text style={s.emptyText}>Search to find nearby EV stations</Text>
        </View>
      ) : stations.length === 0 && !loading ? (
        <View style={s.emptyState}>
          <Text style={s.emptyIcon}>🔍</Text>
          <Text style={s.emptyText}>No stations found. Try a larger radius.</Text>
        </View>
      ) : (
        <FlatList
          data={stations}
          keyExtractor={item => String(item.id)}
          contentContainerStyle={{ padding: 12 }}
          ListHeaderComponent={
            <Text style={s.resultCount}>{stations.length} stations found</Text>
          }
          renderItem={({ item }) => (
            <TouchableOpacity
              style={s.card}
              onPress={() => navigation.navigate('StationDetail', { station: item })}
            >
              <View style={s.cardTop}>
                <Text style={s.cardName} numberOfLines={1}>{item.name}</Text>
                <View style={[s.badge, { borderColor: statusColor(item.status) }]}>
                  <Text style={[s.badgeText, { color: statusColor(item.status) }]}>{item.status}</Text>
                </View>
              </View>
              <Text style={s.cardAddress} numberOfLines={1}>
                {[item.address, item.city, item.state].filter(Boolean).join(', ') || 'Address unavailable'}
              </Text>
              <View style={s.chips}>
                {item.connectors.slice(0, 2).map((c, i) => (
                  <View key={i} style={s.chip}><Text style={s.chipText}>{c}</Text></View>
                ))}
                <View style={s.chip}><Text style={s.chipText}>⚡ {item.num_points} pts</Text></View>
              </View>
            </TouchableOpacity>
          )}
        />
      )}
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  safe: { flex: 1, backgroundColor: C.bg },
  header: { paddingHorizontal: 20, paddingVertical: 14, borderBottomWidth: 1, borderBottomColor: C.border, backgroundColor: C.surface },
  logo: { fontSize: 22, fontWeight: '800', color: C.text },
  logoGreen: { color: C.accent },
  panel: { backgroundColor: C.surface, padding: 16, borderBottomWidth: 1, borderBottomColor: C.border },
  row: { flexDirection: 'row', gap: 10, marginBottom: 10, alignItems: 'flex-end' },
  inputGroup: { flex: 1 },
  label: { fontSize: 10, letterSpacing: 1, color: C.muted, marginBottom: 4 },
  input: { backgroundColor: C.surface2, borderWidth: 1, borderColor: C.border, color: C.text, padding: 9, borderRadius: 6, fontSize: 13 },
  locBtn: { flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderColor: C.accent, borderRadius: 6, paddingHorizontal: 12, paddingVertical: 9, flex: 1, justifyContent: 'center' },
  locBtnText: { color: C.accent, fontSize: 12, fontWeight: '600' },
  searchBtn: { backgroundColor: C.accent, padding: 13, borderRadius: 6, alignItems: 'center' },
  searchBtnText: { color: C.bg, fontWeight: '700', fontSize: 14 },
  emptyState: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 8 },
  emptyIcon: { fontSize: 36 },
  emptyText: { color: C.muted, fontSize: 13 },
  resultCount: { fontSize: 11, color: C.muted, letterSpacing: 1, marginBottom: 8, textTransform: 'uppercase' },
  card: { backgroundColor: C.surface2, borderWidth: 1, borderColor: C.border, borderRadius: 8, padding: 14, marginBottom: 8 },
  cardTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 4 },
  cardName: { flex: 1, color: C.text, fontWeight: '700', fontSize: 14, marginRight: 8 },
  badge: { borderWidth: 1, borderRadius: 20, paddingHorizontal: 8, paddingVertical: 2 },
  badgeText: { fontSize: 10, fontWeight: '600' },
  cardAddress: { color: C.muted, fontSize: 12, marginBottom: 8 },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  chip: { backgroundColor: C.surface, borderWidth: 1, borderColor: C.border, borderRadius: 4, paddingHorizontal: 8, paddingVertical: 3 },
  chipText: { color: C.muted, fontSize: 11 },
});
