const int RAIN_SENSOR_PIN = 34;

// --- HIEU CHINH CHO BUOI THUYET TRINH (XIT NHE NUOC) ---
// Gia tri Avg khi cam bien KHO RAO (so cao hon)
int dryAvg = 250;

// Gia tri Avg khi XIT NHE NUOC (so thap hon, dat cao hon 0 mot chut de nhay khi xit it)
int wetAvg = 80;

// Nguong phat hien mua tinh theo muc giam (drop = dryAvg - avgVal)
// Xit nhe drop tang len -> vuot qua RAIN_DROP_THRESHOLD se bao DANG MUA
const int RAIN_DROP_THRESHOLD = 35;

float smoothAvg = 0;
bool hasInit = false;

void setup() {
  Serial.begin(115200);
  delay(500);

  analogReadResolution(12);
  analogSetPinAttenuation(RAIN_SENSOR_PIN, ADC_11db);

  Serial.println("=== TEST CAM BIEN MUA MKE-S12 (XIT NUOC GIAM VE 0 = DANG MUA) ===");
}

void loop() {
  const int SAMPLES = 12;
  long sum = 0;

  for (int i = 0; i < SAMPLES; i++) {
    sum += analogRead(RAIN_SENSOR_PIN);
    delay(4);
  }

  int rawAvg = sum / SAMPLES;

  // Loc lam muot (EMA) de giam cac cu nhay so dot ngot
  if (!hasInit) {
    smoothAvg = rawAvg;
    hasInit = true;
  } else {
    smoothAvg = (0.7f * smoothAvg) + (0.3f * rawAvg);
  }

  int currentAvg = (int)round(smoothAvg);

  // Khi xit nuoc, currentAvg giam xuong -> drop (muc giam) tang len
  int drop = dryAvg - currentAvg;
  int span = max(1, dryAvg - wetAvg);

  int rainPercent = 0;
  if (drop > 10) {
    rainPercent = map(drop, 10, span, 0, 100);
    rainPercent = constrain(rainPercent, 0, 100);
  }

  String status;
  if (drop < RAIN_DROP_THRESHOLD) {
    status = "KHO RAO";
  } else if (rainPercent < 50) {
    status = "CO NUOC NHE (DANG MUA NHE)";
  } else {
    status = "DANG MUA";
  }

  Serial.print("Avg: ");
  Serial.print(currentAvg);
  Serial.print(" | Giam (Drop): ");
  Serial.print(drop);
  Serial.print(" | Muc mua: ");
  Serial.print(rainPercent);
  Serial.print("% | Trang thai: ");
  Serial.println(status);

  delay(250);
}