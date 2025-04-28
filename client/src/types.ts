export enum Permissions {
  can_upload_plx_files = 'can_upload_plx_files',
  can_use_generator = 'can_use_generator',
  can_upload_files = 'can_upload_files',
  can_edit_rpd = "can_edit_rpd",
  scientific_admin = "scientific_admin",
}

export interface PlanLineItem {
  status: string,
  link_id: number,
  person: number,
  id: number,
  dis: string,
  plan__abbrprofile: string,
  plan__startyear: string,
  newdisid: string,
  caf: string,
}

export interface PlanFileData {
  id: number,
  user_id: number,
  title: string,
  file: string,
  status: number,
  status_verbose: string,
}

export interface PlanDocumentData {
  id: number,
  created_at: string,
  updated_at: string,
  is_deleted: boolean,
  plan_id: number,
  name: string,
  type: number,
  synchronize: boolean,
  manual: boolean,
}

export interface PlanLineData {
  id: number,
  created_at: string,
  updated_at: string,
  is_deleted: boolean,
  plan_id: number,
  disid_id: number,
  dis: string,
  newdisid: string,
  mustbesdudied: number,
  hoursinzet: number,
  caf: number,
  nocalccontrol: boolean,
  type: number,
  viewpract: number,
  viewobject: number,
  kompetences: string,
  synchronize: boolean,
}

export interface PlanSemestrData {
  id: number,
  created_at: string,
  updated_at: string,
  is_deleted: boolean,
  planlineid_id: number,
  num: number,
  lekc: number,
  lab: number,
  pr: number,
  srs: number,
  ekzhour: number,
  zet: number,
  ekz: boolean,
  zach: boolean,
  kp_hour: number,
  kp: boolean,
  kr_hour: number,
  kr: boolean,
  zacho: number,
  eios: number,
}

export interface GeneratorDisciplineIndicatorData {
  id: number,
  indicator_id: number,
  planlineid_id: number,
  know: string,
  able: string,
  own: string,
  criteria: string,
  methods: string,
}

export interface PlanIndicatorData {
  id: number,
  created_at: string,
  updated_at: string,
  is_deleted: boolean,
  planlineid_id: number,
  competence_index: string,
  competence: string,
  indicator_index: string,
  indicator: string,
  discipline_indicator: GeneratorDisciplineIndicatorData[],
}

export interface PlanData {
  id: number,
  created_at: string,
  updated_at: string,
  is_deleted: boolean,
  file_id: number,
  subtype: string,
  shifr: string,
  abbrprofile: string,
  studyform: string,
  studylevel: string,
  studyprog: string,
  elementsinweek: number,
  species: string,
  usernum: number,
  whoratif: string,
  planname: string,
  kafcode: number,
  startyear: number,
  dviga: boolean,
  gviga: boolean,
  igazetweek: number,
  igahourzet: number,
  semesteroncource: number,
  gosdate: string,
  lastshifr: string,
  napr_e: string,
  napr_t: string,
  vuzname: string,
  head: string,
  faculty: string,
}

export interface GeneratorListData {
  discpl: string,
  id_discpl: number,
  planlin: number,
  abbr: string,
  yr: number,
  id_admission: number,
  mira_id: number,
  type: Array,
  person: string,
  id: number,
  status: number,
  status_verbose: string,
  kafcode: number,
  discode: string,
}

export interface GeneratorPlanLineData {
  id: number,
  plan_id: number,
  disid_id: number,
  dis: string,
  newdisid: string,
  mustbesdudied: number,
  hoursinzet: number,
  caf: number,
  nocalccontrol: boolean,
  type: number,
  viewpract: number,
  viewobject: number,
  kompetences: string,
  synchronize: boolean,
  semesters: PlanSemestrData[],
  indicators: PlanIndicatorData[],
  plan: PlanData[],
}

export interface AdmissionInfo {
  id: number,
  yr: number,
  abbr: string,
  cuchplan_id: number,
  spec_name: string,
  direct_name: string,
  kvalif_name: string;
  ckaf_id: number;
  cfac_id: number;
  ckaf__name: string;
  cfac__name: string;
  cadmkind: number;
  cadmkind__name: string;
  cadmkind__name_prof: string;
  cdirection: number;
  cdirection__name: string;
  cdirection__cod: string;
  cfob: number;
  cfob__name: string;
}

export interface OtherDiscipline {
  disid: number,
  dis: string;
}

export interface GeneratorData {
  admission: AdmissionInfo,
  planlines: GeneratorPlanLineData,
  other_discipline: OtherDiscipline[],
  discipline_themes: DisciplineThemesData[],
  discipline_work_hour: DisciplineWorkHour[],
  id: number,
  cadmission: number,
  mira_id: number,
  person: number,
  status: number,
  status_verbose: string,
  precedence_discipline: Array<number>,
  subsequent_discipline: Array<number>,
  library: GeneratorBookData[],
  software: GeneratorSoftwareData[],
  logistics: GeneratorOborudData[],
  recources: DefaultRecources[],
  interactive_methods: string,
  resources: {
    id: number;
    name: string;
    type: number;
    url: string;
  }[];
  comment: null;
  old: {
    abbrprofile: string;
    startyear: number;
    id: number;
    species: string;
  }[];
   new: {
    abbrprofile: string;
    startyear: number;
    id: number;
    species: string;
  }[];
  protocol_number: null;
  protocol_date: null;
  user_accepted_id: null;
  user_type: null;
  meeting: null;
  review_date: null;
  accept_date: null;
  additional_info: any[]; // Можно уточнить тип, если известна структура
}

export interface GeneratorBookData {
  id: number,
  idd: number,
  irbisid: string,
  bib_disc: string,
  rubrica: string,
  title: string,
  avtors: string,
  cnt: number,
  year_izd: number,
  http_link: string,
  izd_type: string,
  place: string,
}

export interface GeneratorSoftwareData {
  id: number,
  cnt: number,
  clicense__name: string,
}

export interface GeneratorOborudData {
  id: number,
  name: string,
  inv: string,
  caud__name: string,
}

export interface GeneratorFormControlData {
  id: number,
  name: string,
}

export interface GeneratorIndependentTypesData {
  id: number,
  name: string,
}

export interface DisciplineThemesData {
  id: number,
  planlineslink_id: number,
  name: string,
  num: number,
  hours: number,
  semester: number,
  formcontrol_id: number,
  formcontrol_verbose: string,
  comment: string,
}

export interface DisciplineWorkHour {
  id: number,
  planlineslink_id: number,
  theme_id: number,
  type: number,
  name: string,
  hours: number,
  semester: number,
}

export interface DefaultRecources {
  id: number,
  name: string,
  type: number,
  url: string,
}
