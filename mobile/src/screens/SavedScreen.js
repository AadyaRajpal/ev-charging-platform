import { View, Text, FlatList, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSaved } from '../context/SavedContext';

const C = {
  bg: '#0a0f0d', surface: '#111812', surface2: '#172019',
  border: '#1e2e21', accent: '#00ff87', text: '#e8f5ec',
  muted: '#6b8c72', red: '#ff4d6a', yellow: '#ffd166',
};

export default function SavedScreen({ navigation }) {
  const { saved, toggleSaved } = useSaved();

  function statusColor(status) {
    if (status === 'Available') return C.accent;
    if (status === 'Unavailable') return C.red;
    return C.yellow;
  }

  if (saved.length === 0) {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.header}>
          <Text style={s.logo}><Text style={s.logoGreen}>EV</Text>Find</Text>
        </View>
        <View style={s.empty}>
          <Ionicons name="bookmark-outline" size={48} color={C.muted} />
          <Text style={s.emptyTitle}>No saved stations</Text>
          <Text style={s.emptyText}>Bookmark stations from the search or detail screen.</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={s.safe}>
      <View style={s.header}>
        <Text style={s.logo}><Text style={s.logoGreen}>EV</Text>Find</Text>
        <Text style={s.count}>{saved.length} saved</Text>
      </View>
      <FlatList
        data={saved}
        keyExtractor={item => String(item.id)}
        contentContainerStyle={{ padding: 12 }}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={s.card}
            onPress={() => navigation.navigate('StationDetail', { station: item })}
          >
            <View style={s.cardTop}>
              <Text style={s.cardName} numberOfLines={1}>{item.name}</Text>
              <TouchableOpacity onPress={() => toggleSaved(item)} hitSlop={10}>
                <Ionicons name="bookmark" size={18} color={C.accent} />
              </TouchableOpacity>
            </View>
            <Text style={s.cardAddress} numberOfLines={1}>
              {[item.address, item.city, item.state].filter(Boolean).join(', ') || 'Address unavailable'}
            </Text>
            <View style={s.cardBottom}>
              <View style={[s.badge, { borderColor: statusColor(item.status) }]}>
                <Text style={[s.badgeText, { color: statusColor(item.status) }]}>{item.status}</Text>
              </View>
              <Text style={s.operator}>{item.operator}</Text>
            </View>
          </TouchableOpacity>
        )}
      />
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  safe: { flex: 1, backgroundColor: C.bg },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 16, backgroundColor: C.surface, borderBottomWidth: 1, borderBottomColor: C.border },
  logo: { fontSize: 20, fontWeight: '800', color: C.text },
  logoGreen: { color: C.accent },
  count: { fontSize: 12, color: C.muted },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 10, padding: 40 },
  emptyTitle: { color: C.text, fontSize: 16, fontWeight: '700' },
  emptyText: { color: C.muted, fontSize: 13, textAlign: 'center', lineHeight: 20 },
  card: { backgroundColor: C.surface2, borderWidth: 1, borderColor: C.border, borderRadius: 8, padding: 14, marginBottom: 8 },
  cardTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 },
  cardName: { flex: 1, color: C.text, fontWeight: '700', fontSize: 14, marginRight: 8 },
  cardAddress: { color: C.muted, fontSize: 12, marginBottom: 8 },
  cardBottom: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  badge: { borderWidth: 1, borderRadius: 20, paddingHorizontal: 8, paddingVertical: 2 },
  badgeText: { fontSize: 10, fontWeight: '600' },
  operator: { color: C.muted, fontSize: 11, flex: 1 },
});
