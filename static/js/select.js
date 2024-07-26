let geo = [
  {
    name: 'Argentina',
    value: 'Argentina',
  },
  {
    name: 'Australia',
    value: 'Australia',
  },
  {
    name: 'Austria',
    value: 'Austria',
  },
  {
    name: 'Belgium',
    value: 'Belgium',
  },
  {
    name: 'Brazil',
    value: 'Brazil',
  },
  {
    name: 'Bulgaria',
    value: 'Bulgaria',
  },
  {
    name: 'Canada',
    value: 'Canada',
  },
  {
    name: 'Chile',
    value: 'Chile',
  },
  {
    name: 'China',
    value: 'China',
  },
  {
    name: 'Colombia',
    value: 'Colombia',
  },
  {
    name: 'Croatia',
    value: 'Croatia',
  },
  {
    name: 'Czech Republic',
    value: 'Czech Republic',
  },
  {
    name: 'Denmark',
    value: 'Denmark',
  },
  {
    name: 'Estonia',
    value: 'Estonia',
  },
  {
    name: 'Finland',
    value: 'Finland',
  },
  {
    name: 'France',
    value: 'France',
  },
  {
    name: 'Germany',
    value: 'Germany',
  },
  {
    name: 'Greece',
    value: 'Greece',
  },
  {
    name: 'Hungary',
    value: 'Hungary',
  },
  {
    name: 'India',
    value: 'India',
  },
  {
    name: 'Ireland',
    value: 'Ireland',
  },
  {
    name: 'Israel',
    value: 'Israel',
  },
  {
    name: 'Italy',
    value: 'Italy',
  },
  {
    name: 'Japan',
    value: 'Japan',
  },
  {
    name: 'Latvia',
    value: 'Latvia',
  },
  {
    name: 'Lithuania',
    value: 'Lithuania',
  },
  {
    name: 'Luxembourg',
    value: 'Luxembourg',
  },
  {
    name: 'Malaysia',
    value: 'Malaysia',
  },
  {
    name: 'Mexico',
    value: 'Mexico',
  },
  {
    name: 'Netherlands',
    value: 'Netherlands',
  },
  {
    name: 'New Zealand',
    value: 'New Zealand',
  },
  {
    name: 'Nigeria',
    value: 'Nigeria',
  },
  {
    name: 'Norway',
    value: 'Norway',
  },
  {
    name: 'Poland',
    value: 'Poland',
  },
  {
    name: 'Portugal',
    value: 'Portugal',
  },
  {
    name: 'Romania',
    value: 'Romania',
  },
  {
    name: 'Russia',
    value: 'Russia',
  },
  {
    name: 'Saudi Arabia',
    value: 'Saudi Arabia',
  },
  {
    name: 'Singapore',
    value: 'Singapore',
  },
  {
    name: 'Slovakia',
    value: 'Slovakia',
  },
  {
    name: 'Slovenia',
    value: 'Slovenia',
  },
  {
    name: 'South Africa',
    value: 'South Africa',
  },
  {
    name: 'Spain',
    value: 'Spain',
  },
  {
    name: 'Sweden',
    value: 'Sweden',
  },
  {
    name: 'Switzerland',
    value: 'Switzerland',
  },
  {
    name: 'Thailand',
    value: 'Thailand',
  },
  {
    name: 'Turkey',
    value: 'Turkey',
  },
  {
    name: 'Ukraine',
    value: 'Ukraine',
  },
  {
    name: 'United Kingdom',
    value: 'United Kingdom',
  },
  {
    name: 'United States',
    value: 'United States',
  },
]
let succesful = [
  {
    name: 'checked',
    value: 'checked',
  },
  {
    name: 'unchecked',
    value: 'unchecked',
  }
]
let status = [
  {
    name: 'stop',
    value: 'stop',
  },
  {
    name: 'wait',
    value: 'wait',
  },
  {
    name: 'run',
    value: 'run',
  }
]
let type = [
  {
    name: 'No email',
    value: '0',
  },
  {
    name: 'Email',
    value: '1',
  }
]
let typeInvoice = [
  {
    name: 'Capitalist',
    value: 'capitalist',
  },
  {
    name: 'USDT',
    value: 'usdt',
  },
  {
    name: 'Bank ',
    value: 'bank ',
  }
]
let format = [
  {
    name: 'Redirect',
    value: 'Redirect',
  },
  {
    name: 'no redirect',
    value: 'no redirect',
  }
]
let userFormatModal = [
  {
    name: 'Redirect',
    value: 'redirect',
  },
  {
    name: 'Banner',
    value: 'banner',
  },
  {
    name: 'Pop',
    value: 'pop',
  }
]
let userSource = [
  {
    name: 'STANDART',
    value: 'STANDART',
  },
  {
    name: 'GOLD',
    value: 'GOLD',
  },
  {
    name: 'PREMIUM',
    value: 'PREMIUM',
  }
]
let payType = [
  {
    name: 'Capitalist',
    value: 'capitalist',
  },
  {
    name: 'USDT',
    value: 'usdt',
  },
  {
    name: 'Bank',
    value: 'bank',
  }
]
let os = [
  {
    name: 'Android',
    value: 'Android',
  },
  {
    name: 'IOS',
    value: 'IOS',
  },
  {
    name: 'Windows',
    value: 'Windows',
  },
  {
    name: 'macOS',
    value: 'macOS',
  },
  {
    name: 'Linux',
    value: 'Linux',
  }
]
let manager = [
  {
    name: 'mail@mail.ru',
    value: 'mail@mail.ru',
  },
  {
    name: 'mail@mail.ru2',
    value: 'mail@mail.ru2',
  },
  {
    name: 'mail@mail.ru3',
    value: 'mail@mail.ru3',
  },
  {
    name: 'mail@mail.ru4',
    value: 'mail@mail.ru4',
  },
  {
    name: 'mail@mail.ru5',
    value: 'mail@mail.ru5',
  },
  {
    name: 'mail@mail.ru6',
    value: 'mail@mail.ru6',
  },
]

let statusSelect = document?.querySelector('#status')
let geoSelect = document?.querySelector('#geo')
let modalGeoSelect = document?.querySelector('#modal-geo')
let typeSelect = document?.querySelector('#type')
let typeInvoceSelect = document?.querySelector('#type-invoce')
let userTypeInvoceSelect = document?.querySelector('#user-payments-type')
let formatSelect = document?.querySelector('#format')
let formatUserModalSelect = document?.querySelector('#format-user-modal')
let succesfulSelect = document?.querySelector('#succesful')
let managerfulSelect = document?.querySelector('#manager')
let managerModalfulSelect = document?.querySelector('#manager-modal')
let modalTypeSelect = document?.querySelector('#modal-type')
let osSelect = document?.querySelector('#os')
let modalUserSourceSelect = document?.querySelector('#modal-user-source')
let modalSourceSelect = document?.querySelector('#modal-source')
let modalFormatSelect = document?.querySelector('#modal-format')
let adminModalCampaignSelect = document?.querySelector('#modal-user')
let _statusSelect;
let _geoSelect;
let _modalGeoSelect;
let _typeSelect;
let _typeInvoceSelect;
let _userTypeInvoceSelect;
let _formatSelect;
let _formatUserModalSelect;
let _succesfulSelect;
let _managerfulSelect;
let _managerModalfulSelect;
let _modalTypeSelect;
let _osSelect;
let _modalUserSourceSelect;
let _modalSourceSelect;
let _modalFormatSelect;
let _adminModalCampaignSelect;
//
// if (statusSelect) {
//   _statusSelect = new Treeselect({
//     parentHtmlContainer: statusSelect,
//     value: '',
//     options: status,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (geoSelect) {
//   _geoSelect = new Treeselect({
//     parentHtmlContainer: geoSelect,
//     value: '',
//     options: geo,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//     saveScrollPosition: false,
//   })
// }
// if (modalGeoSelect) {
//   _modalGeoSelect = new Treeselect({
//     parentHtmlContainer: modalGeoSelect,
//     value: '',
//     options: geo,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//     saveScrollPosition: false,
//   })
// }
// if (formatSelect) {
//   _formatSelect = new Treeselect({
//     parentHtmlContainer: formatSelect,
//     value: '',
//     options: format,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (typeSelect) {
//   _typeSelect = new Treeselect({
//     parentHtmlContainer: typeSelect,
//     value: '',
//     options: type,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (typeInvoceSelect) {
//   _typeInvoceSelect = new Treeselect({
//     parentHtmlContainer: typeInvoceSelect,
//     value: '',
//     options: typeInvoice,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (userTypeInvoceSelect) {
//   _userTypeInvoceSelect = new Treeselect({
//     parentHtmlContainer: userTypeInvoceSelect,
//     value: '',
//     options: payType,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (modalTypeSelect) {
//   _modalTypeSelect = new Treeselect({
//     parentHtmlContainer: modalTypeSelect,
//     value: '',
//     options: type,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (osSelect) {
//   _osSelect = new Treeselect({
//     parentHtmlContainer: osSelect,
//     value: '',
//     options: os,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (modalSourceSelect) {
//   _modalSourceSelect = new Treeselect({
//     parentHtmlContainer: modalSourceSelect,
//     value: '',
//     options: os,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (modalUserSourceSelect) {
//   _modalUserSourceSelect = new Treeselect({
//     parentHtmlContainer: modalUserSourceSelect,
//     value: '',
//     options: userSource,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (modalFormatSelect) {
//   _modalFormatSelect = new Treeselect({
//     parentHtmlContainer: modalFormatSelect,
//     value: '',
//     options: os,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
// if (formatUserModalSelect) {
//   _formatUserModalSelect = new Treeselect({
//     parentHtmlContainer: formatUserModalSelect,
//     value: '',
//     options: userFormatModal,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
//
// if (adminModalCampaignSelect) {
//   _adminModalCampaignSelect = new Treeselect({
//     parentHtmlContainer: adminModalCampaignSelect,
//     value: '',
//     options: manager,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
//
// if (succesfulSelect) {
//   _succesfulSelect = new Treeselect({
//     parentHtmlContainer: succesfulSelect,
//     value: '',
//     options: succesful,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
//
// if (managerfulSelect) {
//   _managerfulSelect = new Treeselect({
//     parentHtmlContainer: managerfulSelect,
//     value: '',
//     options: manager,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
//
// if (managerModalfulSelect) {
//   _managerModalfulSelect = new Treeselect({
//     parentHtmlContainer: managerModalfulSelect,
//     value: '',
//     options: manager,
//     isSingleSelect: true,
//     direction: 'bottom',
//     clearable: false,
//     searchable: false,
//     placeholder: 'Select',
//   })
// }
