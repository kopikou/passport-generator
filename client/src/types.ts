export enum Permissions {
  can_upload_plx_files = 'can_upload_plx_files',
  can_use_generator = 'can_use_generator',
  can_upload_files = 'can_upload_files',
  can_edit_rpd = "can_edit_rpd",
  scientific_admin = "scientific_admin",
  can_monitor_rops = "can_monitor_rops",
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
  type: Array<number>,
  person: string,
  id: number,
  status: number,
  status_verbose: string,
  kafcode: number,
  discode: string,
  can_upload_file_directly: boolean
  last_accepted_file_url: string | null
  user_confirmed_name: string
  user_accepted_name: string
  user_confirmed: number
  user_accepted: number
  zavkaf: number
  fac: number
  rop: number
  razrab: number
  zavkaf_name: string
  rop_name: string
  fac_name: string
  razrab_name: string
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
  semesters: number[],
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
  }[]
  common: {
    abbrprofile: string;
    startyear: number;
    id: number;
    species: string;
  }[];
  users: {
    accepted: string | null
    developer: string | null
    confirmed: string | null
  }
  protocol_number: null;
  protocol_date: null;
  user_accepted_id: null;
  user_type: null;
  meeting: null;
  review_date: null;
  accept_date: null;
  can_be_copied_by_anyone: boolean;
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
  formcontrol_list: number,
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

export interface CopyOptions {
  replace: boolean,
  indicators: boolean,
  themes: boolean,
  lections: boolean,
  labs: boolean,
  practices: boolean,
  srs: boolean,
  additional_info_resources: boolean,
  additional_info_interactiveMethods: boolean,
  additional_info_disciplinePlace: boolean,
  additional_info_software: boolean,
  additional_info_logistics: boolean,
  additional_info_guidelines: boolean,
  additional_info_library: boolean,
  additional_info_tat: boolean,
  additional_info_fos: boolean,
}

export interface RopMonitoring {
  id: number,
  name: string,
  year: number
}

export interface Indicator {
  id: number,
  name: string,
}

export interface RopMonitoringScore {
  id: number,
  rop_monitoring: number | RopMonitoring,
  admission: number,
  person: number,
  indicator: number | Indicator,
  score: number,
}

export interface Admission {
  id: number,
  name: string,
  rop_id: number,
  rop_name: string,
  avg_abit_score: number,
  ratio_CR: number,
  ratio_celev_CR: number,
  abit_score_points: number,
  ratio_CR_points: number,
  ratio_celev_CR_points: number,
  npr_score:number,
  npr_points: number,
  stud_sop_score:number,
  stud_sop_points: number,
  employer_score: number,
  employer_points: number
}

export enum MonitoringIndicators {
  EGE = 4,
  STUD_CONTINGENT = 5,
  CELEV_STUD_CONTINGENT = 6,
  NPR = 7,
  STUD_SOP = 8,
  EMPLOYER = 9,
}
