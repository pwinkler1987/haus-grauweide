// Werbung (AdMob) und der Kauf „Werbung entfernen“. Beides gibt es nur in der
// App; im Browser bleibt das Spiel werbefrei und ohne Kauf.
import { getItem, setItem } from './storage.js';
import { TEST_ADS } from './ads-config.js';

const INTERSTITIAL_ID = TEST_ADS ? {
  android: 'ca-app-pub-3940256099942544/1033173712',
  ios: 'ca-app-pub-3940256099942544/4411468910',
} : {
  android: 'ca-app-pub-3910049405256581/5359005908',
  ios: 'ca-app-pub-3910049405256581/7793597554',
};
const PRODUCT_ID = 'remove_ads';
const NO_ADS_KEY = 'grauweide_no_ads';
const FIRST_AD_AFTER_MS = 4 * 60 * 1000;
const AD_INTERVAL_MS = 5 * 60 * 1000;

const plugins = () => window.Capacitor?.Plugins ?? {};
const platform = () => window.Capacitor?.getPlatform?.();

export class Shop {
  constructor() {
    this.native = !!window.Capacitor?.isNativePlatform?.();
    this.noAds = !this.native;
    this.product = null;  // aus dem Store, für Titel und Preis
    this.adReady = false;
    this.privacyForm = false;
    this.lastAd = performance.now() - AD_INTERVAL_MS + FIRST_AD_AFTER_MS;
  }

  async init() {
    if (!this.native) return;
    this.noAds = (await getItem(NO_ADS_KEY)) === '1';
    await this.loadStore().catch((err) => console.warn('Store:', err));
    if (!this.noAds) await this.startAds().catch((err) => console.warn('AdMob:', err));
  }

  async loadStore() {
    const store = plugins().NativePurchases;
    if (!store || !(await store.isBillingSupported()).isBillingSupported) return;
    await this.checkPurchases();
    const { products } = await store.getProducts({ productIdentifiers: [PRODUCT_ID], productType: 'inapp' });
    this.product = products[0] ?? null;
  }

  async checkPurchases() {
    const { purchases } = await plugins().NativePurchases.getPurchases({ productType: 'inapp' });
    if (purchases.some((p) => p.productIdentifier === PRODUCT_ID && p.purchaseState !== 'pending')) {
      await this.unlock();
    }
  }

  async unlock() {
    this.noAds = true;
    this.adReady = false;
    await setItem(NO_ADS_KEY, '1');
  }

  async startAds() {
    const ads = plugins().AdMob;
    if (!ads) return;
    try {
      const consent = await ads.requestConsentInfo();
      if (consent.status === 'REQUIRED' && consent.isConsentFormAvailable) await ads.showConsentForm();
      this.privacyForm = consent.privacyOptionsRequirementStatus === 'REQUIRED';
    } catch (err) {
      // z. B. keine DSGVO-Mitteilung in AdMob angelegt; Werbung trotzdem laden
      console.warn('Einwilligung:', err);
    }
    if (platform() === 'ios' && (await ads.trackingAuthorizationStatus()).status === 'notDetermined') {
      await ads.requestTrackingAuthorization();
    }
    await ads.initialize({ initializeForTesting: TEST_ADS });
    ads.addListener('interstitialAdDismissed', () => this.prepareAd());
    ads.addListener('interstitialAdFailedToShow', () => this.prepareAd());
    await this.prepareAd();
  }

  async prepareAd() {
    this.adReady = false;
    if (this.noAds) return;
    try {
      await plugins().AdMob.prepareInterstitial({
        adId: INTERSTITIAL_ID[platform()], isTesting: TEST_ADS, immersiveMode: true,
      });
      this.adReady = true;
    } catch (err) {
      console.warn('Werbung nicht geladen:', err);
      setTimeout(() => this.prepareAd(), 60 * 1000);
    }
  }

  // Beim Raumwechsel: höchstens alle paar Minuten eine Vollbildwerbung.
  // Wartet, bis sie geschlossen ist.
  async maybeShowAd() {
    if (this.noAds || !this.adReady || performance.now() - this.lastAd < AD_INTERVAL_MS) return;
    const ads = plugins().AdMob;
    this.adReady = false;
    this.lastAd = performance.now();
    const closed = new Promise((resolve) => {
      const handles = ['interstitialAdDismissed', 'interstitialAdFailedToShow']
        .map((event) => ads.addListener(event, done));
      async function done() {
        for (const h of handles) (await h).remove();
        resolve();
      }
    });
    try {
      await ads.showInterstitial();
      await closed;
    } catch (err) {
      console.warn('Werbung nicht gezeigt:', err);
    }
  }

  get canBuy() {
    return !this.noAds && !!this.product;
  }

  async buy() {
    await plugins().NativePurchases.purchaseProduct({ productIdentifier: PRODUCT_ID, productType: 'inapp' });
    await this.unlock();
  }

  async restore() {
    await plugins().NativePurchases.restorePurchases();
    await this.checkPurchases();
    return this.noAds;
  }

  showPrivacyOptions() {
    return plugins().AdMob.showPrivacyOptionsForm();
  }
}
