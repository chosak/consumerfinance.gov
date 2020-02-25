import Chart from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/Chart.js';
import landingMap from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/landing-map.js';
import { simulateEvent } from '../../../../util/simulate-event';

jest.mock( '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/Chart.js' );

const HTML_SNIPPET = `
<section id="chart-section" class="chart">
    <a href="blah/foo?dataNormalization=None" id="all-results">All</a>
    <div id="landing-map"><div><span><a></a></span></div></div>
  <div class="per-capita m-btn-group">
    <p>Map Shading</p>
    <button class="a-btn raw selected">Complaints</button>
    <button class="a-btn capita a-btn__disabled">Complaints per 1,000</button>
  </div>
</section>
`;

describe( 'The app', () => {
  let idLink, perCapBtn, rawBtn, linkAttr;

  beforeEach( () => {
    Chart.mockClear();
    document.body.innerHTML = HTML_SNIPPET;
    idLink = document.getElementById( 'all-results' );
    perCapBtn = document.getElementsByClassName( 'capita' )[0];
    rawBtn = document.getElementsByClassName( 'raw' )[0];

    global.fetch = jest.fn().mockImplementation( url => {
      expect( url ).toEqual( 'https://files.consumerfinance.gov/ccdb/hero-map-3y.json' );
      return new Promise( resolve => {
        resolve( {
          json: function() {
            return [ { name: 'AK', fullName: 'Alaska', value: 713, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 0.9653855787913047 }, { name: 'AL', fullName: 'Alabama', value: 10380, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.139866013052358 }, { name: 'AR', fullName: 'Arkansas', value: 4402, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.4782010675821977 }, { name: 'AZ', fullName: 'Arizona', value: 14708, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.159782177421084 }, { name: 'CA', fullName: 'California', value: 98601, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.5293432262656443 }, { name: 'CO', fullName: 'Colorado', value: 10643, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.9576865269853743 }, { name: 'CT', fullName: 'Connecticut', value: 7897, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.196981035911195 }, { name: 'DC', fullName: 'District of Columbia', value: 3704, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 5.5086995513027395 }, { name: 'DE', fullName: 'Delaware', value: 3387, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 3.588942623541429 }, { name: 'FL', fullName: 'Florida', value: 86241, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 4.252840466530795 }, { name: 'GA', fullName: 'Georgia', value: 46649, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 4.572698395894384 }, { name: 'HI', fullName: 'Hawaii', value: 2081, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.4637838354934871 }, { name: 'IA', fullName: 'Iowa', value: 2647, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 0.8489138584946868 }, { name: 'ID', fullName: 'Idaho', value: 1849, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.1156195791537824 }, { name: 'IL', fullName: 'Illinois', value: 31170, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.4248268664282135 }, { name: 'IN', fullName: 'Indiana', value: 8446, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.2769075072062275 }, { name: 'KS', fullName: 'Kansas', value: 3553, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.2235606890234243 }, { name: 'KY', fullName: 'Kentucky', value: 5029, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.1366574631089221 }, { name: 'LA', fullName: 'Louisiana', value: 11253, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.4130147116058223 }, { name: 'MA', fullName: 'Massachusetts', value: 12010, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.768955030688645 }, { name: 'MD', fullName: 'Maryland', value: 18317, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 3.0548296645190964 }, { name: 'ME', fullName: 'Maine', value: 1526, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.1472321333255147 }, { name: 'MI', fullName: 'Michigan', value: 16521, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.6644891254586136 }, { name: 'MN', fullName: 'Minnesota', value: 6902, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.2570286697970359 }, { name: 'MO', fullName: 'Missouri', value: 11735, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.9315918555462281 }, { name: 'MS', fullName: 'Mississippi', value: 5230, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.751377996262834 }, { name: 'MT', fullName: 'Montana', value: 1093, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.061307243106358 }, { name: 'NC', fullName: 'North Carolina', value: 25978, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.584216325307653 }, { name: 'ND', fullName: 'North Dakota', value: 753, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.0100942352191555 }, { name: 'NE', fullName: 'Nebraska', value: 1801, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 0.9509372355024313 }, { name: 'NH', fullName: 'New Hampshire', value: 1869, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.403313291006181 }, { name: 'NJ', fullName: 'New Jersey', value: 25600, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.857091518779629 }, { name: 'NM', fullName: 'New Mexico', value: 2725, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.3070622612512879 }, { name: 'NV', fullName: 'Nevada', value: 10974, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 3.800223359218762 }, { name: 'NY', fullName: 'New York', value: 53008, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.6774113319636483 }, { name: 'OH', fullName: 'Ohio', value: 21901, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.8864306881212662 }, { name: 'OK', fullName: 'Oklahoma', value: 4329, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.1110680497740006 }, { name: 'OR', fullName: 'Oregon', value: 5838, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.4503890187812707 }, { name: 'PA', fullName: 'Pennsylvania', value: 25605, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.0018756100716897 }, { name: 'RI', fullName: 'Rhode Island', value: 1884, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.7838577913113627 }, { name: 'SC', fullName: 'South Carolina', value: 13788, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.8176474483002156 }, { name: 'SD', fullName: 'South Dakota', value: 702, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 0.820626481686703 }, { name: 'TN', fullName: 'Tennessee', value: 13730, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.081128860073414 }, { name: 'TX', fullName: 'Texas', value: 72300, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.6367987993411433 }, { name: 'UT', fullName: 'Utah', value: 6252, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.088217503284133 }, { name: 'VA', fullName: 'Virginia', value: 18919, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 2.2614282271760584 }, { name: 'VT', fullName: 'Vermont', value: 702, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.1238545328799492 }, { name: 'WA', fullName: 'Washington', value: 12217, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.703913002667934 }, { name: 'WI', fullName: 'Wisconsin', value: 7234, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.255201738889929 }, { name: 'WV', fullName: 'West Virginia', value: 1540, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 0.8383950070855266 }, { name: 'WY', fullName: 'Wyoming', value: 651, issue: 'Incorrect information on your report', product: 'Credit reporting, credit repair services, or other personal consumer reports', perCapita: 1.1162551440329218 } ];
          }
        } );
      } );
    } );
  } );


  it( 'should not throw any errors on init', () => {
    landingMap.init();
    linkAttr = idLink.getAttribute( 'href' );
    expect( linkAttr ).toBe( 'blah/foo?dataNormalization=None' );
    expect( perCapBtn.classList.contains( 'a-btn__disabled' ) ).toBeTruthy();
    expect( Chart ).toHaveBeenCalledTimes( 1 );
  } );

  describe( 'Per Capita button', () => {
    it( 'switches classes and link when clicked', () => {
      landingMap.init();
      simulateEvent( 'click', perCapBtn );
      linkAttr = idLink.getAttribute( 'href' );
      expect( linkAttr ).toBe( 'blah/foo?dataNormalization=Per%201000%20pop.' );
      expect( rawBtn.classList.contains( 'selected' ) ).toBeFalsy();
      expect( perCapBtn.classList.contains( 'selected' ) ).toBeTruthy();
      expect( Chart ).toHaveBeenCalledTimes( 2 );
    } );
  } );

  describe( 'Complaints button', () => {
    it( 'does not switch classes when already selected', () => {
      landingMap.init();
      simulateEvent( 'click', rawBtn );
      expect( rawBtn.classList.contains( 'selected' ) ).toBeTruthy();
      expect( perCapBtn.classList.contains( 'selected' ) ).toBeFalsy();
    } );

    it( 'switch classes and links when selected twice', () => {
      landingMap.init();
      linkAttr = idLink.getAttribute( 'href' );
      expect( linkAttr ).toBe( 'blah/foo?dataNormalization=None' );
      simulateEvent( 'click', perCapBtn );
      linkAttr = idLink.getAttribute( 'href' );
      expect( rawBtn.classList.contains( 'selected' ) ).toBeFalsy();
      expect( perCapBtn.classList.contains( 'selected' ) ).toBeTruthy();
      expect( linkAttr ).toBe( 'blah/foo?dataNormalization=Per%201000%20pop.' );

      simulateEvent( 'click', rawBtn );
      linkAttr = idLink.getAttribute( 'href' );
      expect( rawBtn.classList.contains( 'selected' ) ).toBeTruthy();
      expect( perCapBtn.classList.contains( 'selected' ) ).toBeFalsy();
      expect( linkAttr ).toBe( 'blah/foo?dataNormalization=None' );

      expect( Chart ).toHaveBeenCalledTimes( 3 );
    } );
  } );
} );
