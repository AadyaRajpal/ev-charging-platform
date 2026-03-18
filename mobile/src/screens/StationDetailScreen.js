import { View, Text, ScrollView, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSaved } from '../context/SavedContext';

const C = {
  bg: '#0a0f0d', surface: '#111812', surface2: '#172019',
  border: '#1e2e21', accent: '#00ff87', text: '#e8f5ec',
  muted: '#6b8c72', red: '#ff4d6a', yellow: '#ffd166',
};

export default function StationDetailScreen({ route, navigation }) {
  const { station: s } = route.params;
  const { toggleSaved, isSaved } = useSaved();
  const saved = isSaved(s.id);

  const statusColor = s.status === 'Available' ? C.accent
    : s.status === 'Unavailable' ? C.red : C.yellow;

  const address = [s.address, s.city, s.state, s.country].filter(Boolean).join(', ');

  return (
    <SafeAreaView style={st.safe}>
      {/* Top bar */}
      <View style={st.topBar}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={st.backBtn}>
          <Ionicons name="arrow-back" size={22} color={C.text} />
        </TouchableOpacity>
        <Text style={st.topTitle} numberOfLines={1}>{s.name}</Text>
        <TouchableOpacity onPress={() => toggleSaved(s)} style={st.saveBtn}>
          <Ionicons name={saved ? 'bookmark' : 'bookmark-outline'} size={22} color={C.accent} />
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={st.content}>
        {/* Status banner */}
        <View style={[st.statusBanner, { borderColor: statusColor }]}>
          <View style={[st.statusDot, { backgroundColor: statusColor }]} />
          <Text style={[st.statusText, { color: statusColor }]}>{s.status}</Text>
        </View>

        {/* Name & address */}
        <Text style={st.name}>{s.name}</Text>
        <Text style={st.address}>{address || 'Address not available'}</Text>

        {/* Info rows */}
        <View style={st.section}>
          <InfoRow icon="business-outline" label="Operator" value={s.operator} />
          <InfoRow icon="flash-outline" label="Charging Points" value={`${s.num_points || '?'} points`} />
          <InfoRow icon="card-outline" label="Usage Cost" value={s.usage_cost || 'Not specified'} />
          <InfoRow icon="location-outline" label="Coordinates" value={`${s.lat?.toFixed(4)}, ${s.lng?.toFixed(4)}`} />
        </View>

        {/* Connectors */}
        {s.connectors.length > 0 && (
          <View style={st.section}>
            <Text style={st.sectionTitle}>CONNECTOR TYPES</Text>
            <View style={st.connectorList}>
              {s.connectors.map((c, i) => (
                <View key={i} style={st.connectorChip}>
                  <Ionicons name="flash" size={12} color={C.accent} />
                  <Text style={st.connectorText}>{c}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {/* Save button */}
        <TouchableOpacity
          style={[st.bigBtn, saved && st.bigBtnSaved]}
          onPress={() => toggleSaved(s)}
        >
          <Ionicons name={saved ? 'bookmark' : 'bookmark-outline'} size={18} color={saved ? C.bg : C.accent} />
          <Text style={[st.bigBtnText, saved && st.bigBtnTextSaved]}>
            {saved ? 'Saved' : 'Save Station'}
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

function InfoRow({ icon, label, value }) {
  return (
    <View style={st.infoRow}>
      <Ionicons name={icon} size={16} color={C.muted} style={st.infoIcon} />
      <View style={st.infoContent}>
        <Text style={st.infoLabel}>{label}</Text>
        <Text style={st.infoValue}>{value}</Text>
      </View>
    </View>
  );
}

const st = StyleSheet.create({
  safe: { flex: 1, backgroundColor: C.bg },
  topBar: { flexDirection: 'row', alignItems: 'center', padding: 16, backgroundColor: C.surface, borderBottomWidth: 1, borderBottomColor: C.border },
  backBtn: { padding: 4, marginRight: 8 },
  topTitle: { flex: 1, color: C.text, fontWeight: '700', fontSize: 15 },
  saveBtn: { padding: 4 },
  content: { padding: 20, gap: 4 },
  statusBanner: { flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderRadius: 8, padding: 10, marginBottom: 16, gap: 8 },
  statusDot: { width: 8, height: 8, borderRadius: 4 },
  statusText: { fontWeight: '700', fontSize: 13 },
  name: { color: C.text, fontSize: 20, fontWeight: '800', marginBottom: 6 },
  address: { color: C.muted, fontSize: 13, marginBottom: 20, lineHeight: 18 },
  section: { backgroundColor: C.surface, borderWidth: 1, borderColor: C.border, borderRadius: 10, padding: 4, marginBottom: 16 },
  sectionTitle: { fontSize: 10, letterSpacing: 1, color: C.muted, padding: 12, paddingBottom: 4 },
  infoRow: { flexDirection: 'row', alignItems: 'flex-start', padding: 12, borderBottomWidth: 1, borderBottomColor: C.border },
  infoIcon: { marginRight: 12, marginTop: 2 },
  infoContent: { flex: 1 },
  infoLabel: { fontSize: 11, color: C.muted, marginBottom: 2 },
  infoValue: { fontSize: 14, color: C.text, fontWeight: '500' },
  connectorList: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, padding: 12 },
  connectorChip: { flexDirection: 'row', alignItems: 'center', gap: 5, backgroundColor: C.surface2, borderWidth: 1, borderColor: C.border, borderRadius: 6, paddingHorizontal: 10, paddingVertical: 6 },
  connectorText: { color: C.text, fontSize: 12 },
  bigBtn: { borderWidth: 1, borderColor: C.accent, borderRadius: 8, padding: 14, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, marginTop: 8 },
  bigBtnSaved: { backgroundColor: C.accent },
  bigBtnText: { color: C.accent, fontWeight: '700', fontSize: 14 },
  bigBtnTextSaved: { color: C.bg },
});
