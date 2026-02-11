import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  StyleSheet,
  TouchableOpacity,
  Text,
  ActivityIndicator,
  Alert,
} from 'react-native';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import { useLocation } from '../context/LocationContext';
import { stationsService } from '../services/apiService';

export default function MapScreen({ navigation }) {
  const { location, loading: locationLoading } = useLocation();
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedStation, setSelectedStation] = useState(null);
  const [filters, setFilters] = useState({
    connector_type: null,
    available_only: true,
  });
  const mapRef = useRef(null);

  useEffect(() => {
    if (location) {
      fetchNearbyStations();
    }
  }, [location, filters]);

  const fetchNearbyStations = async () => {
    if (!location) return;

    setLoading(true);
    try {
      const response = await stationsService.getNearbyStations(
        location.latitude,
        location.longitude,
        5000, // 5km radius
        filters
      );
      setStations(response);
    } catch (error) {
      console.error('Error fetching stations:', error);
      Alert.alert('Error', 'Failed to load charging stations');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkerPress = (station) => {
    setSelectedStation(station);
    // Animate to station
    mapRef.current?.animateToRegion({
      latitude: station.latitude,
      longitude: station.longitude,
      latitudeDelta: 0.01,
      longitudeDelta: 0.01,
    });
  };

  const handleStationPress = (station) => {
    navigation.navigate('StationDetails', { station });
  };

  const getMarkerColor = (station) => {
    // Color based on availability
    const availableChargers = station.chargers?.filter(c => c.available).length || 0;
    if (availableChargers === 0) return '#FF0000'; // Red - No available
    if (availableChargers < 2) return '#FFA500'; // Orange - Limited
    return '#00FF00'; // Green - Available
  };

  if (locationLoading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Getting your location...</Text>
      </View>
    );
  }

  if (!location) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>Location access required</Text>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Enable Location</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Map */}
      <MapView
        ref={mapRef}
        style={styles.map}
        provider={PROVIDER_GOOGLE}
        initialRegion={location}
        showsUserLocation
        showsMyLocationButton
      >
        {stations.map((station) => (
          <Marker
            key={station.station_id}
            coordinate={{
              latitude: station.latitude,
              longitude: station.longitude,
            }}
            pinColor={getMarkerColor(station)}
            onPress={() => handleMarkerPress(station)}
          >
            <View style={styles.markerContainer}>
              <View
                style={[
                  styles.marker,
                  { backgroundColor: getMarkerColor(station) },
                ]}
              >
                <Text style={styles.markerText}>⚡</Text>
              </View>
            </View>
          </Marker>
        ))}
      </MapView>

      {/* Filter Bar */}
      <View style={styles.filterBar}>
        <TouchableOpacity
          style={[
            styles.filterButton,
            filters.connector_type === 'CCS' && styles.filterButtonActive,
          ]}
          onPress={() =>
            setFilters({
              ...filters,
              connector_type: filters.connector_type === 'CCS' ? null : 'CCS',
            })
          }
        >
          <Text style={styles.filterText}>CCS</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.filterButton,
            filters.connector_type === 'CHAdeMO' && styles.filterButtonActive,
          ]}
          onPress={() =>
            setFilters({
              ...filters,
              connector_type: filters.connector_type === 'CHAdeMO' ? null : 'CHAdeMO',
            })
          }
        >
          <Text style={styles.filterText}>CHAdeMO</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.filterButton,
            filters.connector_type === 'Tesla' && styles.filterButtonActive,
          ]}
          onPress={() =>
            setFilters({
              ...filters,
              connector_type: filters.connector_type === 'Tesla' ? null : 'Tesla',
            })
          }
        >
          <Text style={styles.filterText}>Tesla</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.refreshButton}
          onPress={fetchNearbyStations}
        >
          <Text style={styles.refreshText}>🔄</Text>
        </TouchableOpacity>
      </View>

      {/* Station Info Card */}
      {selectedStation && (
        <View style={styles.stationCard}>
          <View style={styles.cardHeader}>
            <Text style={styles.stationName}>{selectedStation.name}</Text>
            <TouchableOpacity onPress={() => setSelectedStation(null)}>
              <Text style={styles.closeButton}>✕</Text>
            </TouchableOpacity>
          </View>

          <Text style={styles.stationAddress}>{selectedStation.address}</Text>

          <View style={styles.stationInfo}>
            <Text style={styles.infoText}>
              ⚡ {selectedStation.chargers?.filter(c => c.available).length || 0} /
              {selectedStation.chargers?.length || 0} Available
            </Text>
            <Text style={styles.infoText}>
              📍 {selectedStation.distance_km?.toFixed(1) || 'N/A'} km
            </Text>
          </View>

          <View style={styles.chargersList}>
            {selectedStation.chargers?.slice(0, 2).map((charger, index) => (
              <View key={index} style={styles.chargerItem}>
                <Text style={styles.chargerType}>{charger.connector_type}</Text>
                <Text style={styles.chargerPower}>{charger.power_kw} kW</Text>
                <Text
                  style={[
                    styles.chargerStatus,
                    { color: charger.available ? '#00FF00' : '#FF0000' },
                  ]}
                >
                  {charger.available ? 'Available' : 'In Use'}
                </Text>
              </View>
            ))}
          </View>

          <TouchableOpacity
            style={styles.detailsButton}
            onPress={() => handleStationPress(selectedStation)}
          >
            <Text style={styles.detailsButtonText}>View Details & Start Charging</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Loading Overlay */}
      {loading && (
        <View style={styles.loadingOverlay}>
          <ActivityIndicator size="large" color="#007AFF" />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  map: {
    flex: 1,
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  errorText: {
    fontSize: 18,
    color: '#FF0000',
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
  },
  buttonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: '600',
  },
  markerContainer: {
    alignItems: 'center',
  },
  marker: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#FFF',
  },
  markerText: {
    fontSize: 20,
  },
  filterBar: {
    position: 'absolute',
    top: 10,
    left: 10,
    right: 10,
    flexDirection: 'row',
    backgroundColor: '#FFF',
    borderRadius: 8,
    padding: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  filterButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    marginHorizontal: 4,
    borderRadius: 6,
    backgroundColor: '#F0F0F0',
    alignItems: 'center',
  },
  filterButtonActive: {
    backgroundColor: '#007AFF',
  },
  filterText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  refreshButton: {
    width: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  refreshText: {
    fontSize: 20,
  },
  stationCard: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: '#FFF',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  stationName: {
    fontSize: 18,
    fontWeight: '700',
    color: '#000',
    flex: 1,
  },
  closeButton: {
    fontSize: 24,
    color: '#666',
    padding: 4,
  },
  stationAddress: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  stationInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  infoText: {
    fontSize: 14,
    color: '#333',
  },
  chargersList: {
    marginBottom: 16,
  },
  chargerItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  chargerType: {
    fontSize: 14,
    fontWeight: '600',
    color: '#000',
    flex: 1,
  },
  chargerPower: {
    fontSize: 14,
    color: '#666',
    flex: 1,
    textAlign: 'center',
  },
  chargerStatus: {
    fontSize: 14,
    fontWeight: '600',
    flex: 1,
    textAlign: 'right',
  },
  detailsButton: {
    backgroundColor: '#007AFF',
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
  },
  detailsButtonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: '600',
  },
  loadingOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0,0,0,0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
});
