# Motion Capture CSV Converter

Una applicazione GUI user-friendly per convertire dati CSV di motion capture in valori applicati alle ossa secondo il dizionario DIZIONARIO.py.

## Caratteristiche

✨ **Interfaccia Grafica Intuitiva** - GUI sviluppata con tkinter, semplice da usare  
📁 **Selezione File CSV** - Dialog per selezionare file CSV di motion capture  
🎞️ **Navigazione Frame** - Slider e input per navigare tra i frame  
🔍 **Filtri Source** - Filtra per face_cap, epic, a2f o visualizza tutti  
📊 **Visualizzazione Risultati** - Tabella organizzata per osso con dettagli  
💾 **Export JSON** - Esporta i risultati processati in formato JSON  
⚡ **Anteprima Live** - Aggiornamento in tempo reale quando si cambia frame  

## Requisiti

- Python 3.6+
- tkinter (incluso in Python)
- pandas
- DIZIONARIO.py (incluso nel repository)

### Installazione Dipendenze

```bash
pip install pandas
```

Su Ubuntu/Debian potrebbe essere necessario installare tkinter:
```bash
sudo apt install python3-tk
```

## Utilizzo

### 1. Avvio dell'Applicazione

```bash
python3 mocap_gui.py
```

### 2. Caricamento File CSV

1. Clicca su "**Select CSV File**"
2. Scegli il file CSV con i dati di motion capture
3. Il file verrà caricato automaticamente e mostrerà il numero di frame disponibili

### 3. Navigazione tra i Frame

- **Slider**: Trascina il cursore per navigare rapidamente
- **Input numerico**: Inserisci un numero specifico e premi Enter
- **Info frame**: Mostra frame corrente / totale frame

### 4. Filtri Source

Seleziona quale tipo di dati visualizzare:
- **All**: Mostra tutti i tipi di source
- **Face Cap**: Solo dati da face_cap
- **Epic**: Solo dati da epic  
- **A2F**: Solo dati da a2f

### 5. Visualizzazione Risultati

La tabella mostra:
- **Parameter**: Nome del parametro CSV originale
- **Value**: Valore numerico dal CSV
- **Bone**: Nome dell'osso di destinazione
- **Object**: Oggetto 3D (es. FaceitControlRig)
- **Transform**: Tipo di trasformazione (LOC_X, LOC_Y, LOC_Z, ROT_X, ROT_Y, ROT_Z)
- **Source**: Fonte del dato (face_cap, epic, a2f)

### 6. Export JSON

1. Naviga al frame desiderato
2. Imposta i filtri source se necessario
3. Clicca "**Export to JSON**"
4. Scegli dove salvare il file JSON

## Formato del CSV

Il CSV deve contenere:
- Colonna `Timecode` con il timecode del frame
- Colonna `BlendShapeCount` con il numero di blend shapes
- Colonne con nomi dei parametri di motion capture (es. `EyeBlinkLeft`, `JawOpen`, etc.)

Esempio:
```csv
Timecode,BlendShapeCount,EyeBlinkLeft,EyeBlinkRight,JawOpen,MouthClose,...
00:00:00:01.001,51,0.11733060,0.06477024,0.01473731,0.00087887,...
```

## Struttura del JSON Esportato

```json
{
  "frame": 10,
  "timecode": "00:00:00:11.011",
  "bones": {
    "c_eyelid_upper.L": {
      "object": "FaceitControlRig",
      "transforms": {
        "eyeBlinkLeft": {
          "value": 0.17235579,
          "transform_type": "LOC_Y",
          "source": "face_cap"
        }
      }
    }
  }
}
```

## Mappatura Dati

L'applicazione usa il file `DIZIONARIO.py` per mappare i parametri CSV alle ossa 3D:

- **PascalCase** nel CSV (es. `EyeBlinkLeft`) → **camelCase** nel dizionario (es. `eyeBlinkLeft`)
- Supporto per varianti con suffissi source (`_face_cap`, `_epic`, `_a2f`)
- Mappatura automatica dei tipi di trasformazione (LOC_X/Y/Z, ROT_X/Y/Z)

## Gestione Errori

L'applicazione include:
- ✅ Validazione input CSV
- ✅ Controllo formato frame
- ✅ Messaggi di errore user-friendly
- ✅ Gestione file mancanti
- ✅ Controllo valori fuori range

## File di Esempio

Il repository include `20250523_170050_blendshape_data.csv` come file di esempio per testare l'applicazione.

## Sviluppo

### Test

Esegui i test inclusi:
```bash
# Test elaborazione logica
python3 test_processing.py

# Test GUI completo (richiede display)
python3 demo_complete.py
```

### Struttura File

- `mocap_gui.py` - Applicazione principale GUI
- `DIZIONARIO.py` - Mappatura parametri → ossa
- `test_*.py` - Script di test e dimostrazione
- `demo_*.png` - Screenshot dell'applicazione

## Supporto

Per problemi o domande, controlla:
1. I messaggi di errore nell'applicazione
2. La console per errori dettagliati
3. La compatibilità del formato CSV
4. La presenza del file DIZIONARIO.py