const BASE_URL = '/data-research/mortgages/api/v1/metadata/';
const cache = {};

let globalZoomLevel = 10;

/**
 * @param {string} dataType - dataType to append to the BASE_URL
 * @param {Function} cb - The callback to pass the data
 * @returns {Promise} The result of calling the callback on the resolved data
 */
function fetcher(dataType, cb) {
  if (cache[dataType]) return Promise.resolve(cb(cache[dataType]));
  return fetch(BASE_URL + dataType)
    .then((v) => v.json())
    .then((v) => cb(v));
}

const utils = {
  /**
   * showEl - Un-hides a page element.
   * @param {object} el - DOM node to un-hide.
   * @returns {object} The un-hidden DOM node.
   */
  showEl: (el) => {
    el.style.display = '';
    return el;
  },

  /**
   * hideEl - Hides a page element.
   * @param {object} el - DOM node to hide.
   * @returns {object} The hidden DOM node.
   */
  hideEl: (el) => {
    el.style.display = 'none';
    return el;
  },

  /**
   * disableEl - Disables a page element. Used for form inputs.
   * @param {object} el - DOM node to disable.
   * @returns {object} The disabled DOM node.
   */
  disableEl: (el) => {
    el.disabled = true;
    return el;
  },

  /**
   * enableEl - Enables a page element. Used for form inputs.
   * @param {object} el - DOM node to enable.
   * @returns {object} The enabled DOM node.
   */
  enableEl: (el) => {
    el.disabled = false;
    return el;
  },

  /**
   * addOption - Create select option to be injected into HTML select element.
   * @param {object} params - A parameters object.
   * @param {HTMLElement} params.document - window.document.
   * @param {string} params.value - <option value="VALUE">text</option>.
   * @param {string} params.text - <option value="value">TEXT</option>.
   * @returns {HTMLElement} The option HTML element node.
   */
  addOption: ({ document, value, text }) => {
    const option = document.createElement('option');
    option.value = value;
    option.text = text;
    return option;
  },

  /**
   * getStateData - XHR state metadata.
   * @param {Function} cb - Function called with state data.
   * @returns {Function} Function called with state data.
   */
  getStateData: (cb) => fetcher('state_meta', cb),

  /**
   * getCountyData - XHR county metadata
   * @param {Function} cb - Function called with county data.
   * @returns {Function} Function called with county data.
   */
  getCountyData: (cb) => fetcher('state_county_meta', cb),

  /**
   * getMetroData - XHR metro metadata
   * @param {Function} cb - Function called with metro data.
   * @returns {Function} Function called with metro data.
   */
  getMetroData: (cb) => fetcher('state_msa_meta', cb),

  /**
   * getNonMetroData - XHR non-metro metadata
   * @param {Function} cb - Function called with non-metro data.
   * @returns {Function} Function called with non-metro data.
   */
  getNonMetroData: (cb) => fetcher('non_msa_fips', cb),

  /**
   * getDate - Convert a date from YYYY-MM-DD to Month YYYY.
   * @param {string} dateString - Date in the format YYYY-MM-DD
   * @returns {string} Date in the format Month YYYY.
   */
  getDate: (dateString) => {
    const dates = dateString.split('-');
    if (dates.length < 2) {
      return dateString;
    }
    const months = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
    ];
    return `${months[parseInt(dates[1], 10) - 1]} ${dates[0]}`;
  },

  /**
   * getCountyState - Get the U.S. state belonging to a county.
   * @param {string} fips - FIPS county code.
   * @returns {string} Two character state abbreviation.
   */
  getCountyState: (fips) => {
    // Grab the first two digits of the county's FIPS code.
    fips = fips.slice(0, 2);
    const usStates = {
      '01': 'AL',
      '02': 'AK',
      '04': 'AZ',
      '05': 'AR',
      '06': 'CA',
      '08': 'CO',
      '09': 'CT',
      10: 'DE',
      11: 'DC',
      12: 'FL',
      13: 'GA',
      15: 'HI',
      16: 'ID',
      17: 'IL',
      18: 'IN',
      19: 'IA',
      20: 'KS',
      21: 'KY',
      22: 'LA',
      23: 'ME',
      24: 'MD',
      25: 'MA',
      26: 'MI',
      27: 'MN',
      28: 'MS',
      29: 'MO',
      30: 'MT',
      31: 'NE',
      32: 'NV',
      33: 'NH',
      34: 'NJ',
      35: 'NM',
      36: 'NY',
      37: 'NC',
      38: 'ND',
      39: 'OH',
      40: 'OK',
      41: 'OR',
      42: 'PA',
      44: 'RI',
      45: 'SC',
      46: 'SD',
      47: 'TN',
      48: 'TX',
      49: 'UT',
      50: 'VT',
      51: 'VA',
      53: 'WA',
      54: 'WV',
      55: 'WI',
      56: 'WY',
      60: 'AS',
      66: 'GU',
      69: 'MP',
      72: 'PR',
      74: 'UM',
      78: 'VI',
    };
    return usStates[fips];
  },

  /**
   * isNonMetro - Check if a location's FIPS code is for a non-metro area.
   * @param {string} fips - FIPS code, e.g. 52435 or 06-non.
   * @returns {boolean} True if it's a non-metro
   */
  isNonMetro: (fips) => fips.indexOf('-non') > -1,

  /**
   * getZoomLevel - Calculate map's zoom level. Highchart's zooming feature
   * takes a `howMuch` parameter to determine how much to zoom the map.
   * Values less than 1 zooms in. 0.5 zooms in to half the current view.
   * 2 zooms to twice the current view. If omitted, the zoom is reset.
   * See https://api.highcharts.com/class-reference/Highcharts.Chart.html#mapZoom
   *
   * This function normalizes the map's zooming by keeping track of the current
   * zoom level and calculating a new one based on the requested amount of zoom.
   * @param {number} zoomLevel - Requested zoom level from 1 to 10, with 10 being
   * zoomed all the way out.
   * @returns {number} Highcharts-compatible zoom level.
   */
  getZoomLevel: (zoomLevel) => {
    const level = zoomLevel / globalZoomLevel;
    globalZoomLevel = zoomLevel;
    return level;
  },

  /**
   * setZoomLevel - Set global normalized zoom level. See above.
   * @param {number} zoomLevel - Global zoom level to store.
   * @returns {number} Global zoom level.
   */
  setZoomLevel: (zoomLevel) => {
    globalZoomLevel = zoomLevel;
    return zoomLevel;
  },

  /**
   * getYear - Returns the year form a date in the format YYYY-MM-DD.
   * @param {string} date - Date in format YYYY-MM-DD.
   * @returns {string} Year as YYYY.
   */
  getYear: (date) => date.split('-')[0],

  /**
   * getMonth - Returns the month form a date in the format YYYY-MM-DD.
   * @param {string} date - Date in format YYYY-MM-DD.
   * @returns {string} Month as MM.
   */
  getMonth: (date) => date.split('-')[1],

  /**
   * isDateValid - Check if date is less than or equal to the provided end date.
   * @param {string} currDate - Date in format YYYY-MM-DD.
   * @param {string} endDate - Date in format YYYY-MM-DD.
   * @returns {boolean} True if date is less than or equal to the provided
   * end date.
   */
  isDateValid: (currDate, endDate) => {
    currDate = currDate.split('-');
    endDate = endDate.split('-');
    // If dates are invalid, abort.
    if (currDate.length === 1 || endDate.length === 1) {
      return false;
    }
    // Is the current year less than the end year?
    if (currDate[0] < endDate[0]) {
      return true;
    }
    // If the years are the same, is the current month less than the end month?
    if (currDate[0] === endDate[0] && currDate[1] <= endDate[1]) {
      return true;
    }
    return false;
  },

  /**
   * stateCentroids - Dictionary of every state's centroid coordinates
   * organized by state abbreviation.
   */
  stateCentroids: {
    AL: [6614, -5006.5],
    AK: [357, -3476.5],
    AZ: [1129.5, -5601],
    AR: [5353, -5486.5],
    CA: [-169.5, -6770.5],
    CO: [2599, -6679],
    CT: [9038, -7795.5],
    DE: [8669, -7063],
    DC: [8363, -6930.5],
    FL: [7381, -3947.5],
    GA: [7331.5, -5141.5],
    HI: [2488.5, -3036.95],
    ID: [1130, -8589],
    IL: [5851, -6820],
    IN: [6492, -6872],
    IA: [5047.5, -7352.5],
    KS: [4061.5, -6458],
    KY: [6660.5, -6353.5],
    LA: [5561.5, -4534.5],
    ME: [9465, -8891],
    MD: [8307, -6973.5],
    MA: [9201, -8040],
    MI: [6341, -8191],
    MN: [5000.5, -8503.5],
    MS: [5894.5, -4964],
    MO: [5283.5, -6413.5],
    MT: [2093, -8873],
    NE: [3823, -7249],
    NV: [410, -6945.5],
    NH: [9135, -8472.5],
    NJ: [8748, -7351.5],
    NM: [2360.5, -5499],
    NY: [8446.5, -8057],
    NC: [7943, -5998],
    ND: [3762, -8803],
    OH: [7153.5, -7106],
    OK: [3979, -5642],
    OR: [-14, -8514.5],
    PA: [8134.5, -7407],
    RI: [9258, -7890],
    SC: [7775.5, -5432.5],
    SD: [3736, -7957.5],
    TN: [6647, -5875],
    TX: [3643, -4555],
    UT: [1404, -6966],
    VT: [8870, -8408],
    VA: [7940.5, -6574],
    WA: [233, -9336.5],
    WV: [7734, -6797],
    WI: [5661, -8084],
    WY: [2328, -7755],
  },

  /**
   * thunkMiddleware - Vanilla JS implementation of redux-thunk.
   * See: https://github.com/gaearon/redux-thunk
   * @param {object} store - The app's store.
   * @returns {Function} Dispatch function with the action provided.
   */
  thunkMiddleware: (store) => (next) => (action) => {
    if (typeof action === 'function') {
      return action(store.dispatch, store.getState);
    }
    return next(action);
  },

  /**
   * loggerMiddleware - Vanilla JS implementation redux-devtools.
   * See: https://github.com/gaearon/redux-devtools
   * @param {object} store - The app's store.
   * @returns {Function} Dispatch function with the action provided.
   */
  loggerMiddleware: (store) => (next) => (action) => {
    if (!window.MP_DEBUG) {
      return next(action);
    }
    console.groupCollapsed(action.type);
    console.group('action:');
    console.log(JSON.stringify(action, '', '\t'));
    console.groupEnd();
    console.groupCollapsed('previous state:');
    console.log(JSON.stringify(store.getState(), '', '\t'));
    console.groupEnd();
    const result = next(action);
    console.groupCollapsed('state:');
    console.log(JSON.stringify(store.getState(), '', '\t'));
    console.groupEnd();
    console.groupEnd();
    return result;
  },
};

export default utils;
