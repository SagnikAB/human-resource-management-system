'use client';
import { Download } from 'lucide-react';
import { PageTransition } from '@/components/shared/PageTransition';
import { AttendanceCalendar } from '@/components/attendance/AttendanceCalendar';
import { CheckInButton } from '@/components/attendance/CheckInButton';
import { WeeklyChart } from '@/components/attendance/WeeklyChart';
import { DataTable } from '@/components/shared/DataTable';
import { StatusBadge } from '@/components/shared/StatusBadge';
import { useAttendance } from '@/hooks/useAttendance';

export default function Attendance(){
  const {data=[]}=useAttendance();
  function exportCsv(){
    const csv=['date,status,checkIn,checkOut',...data.map(r=>`${r.date},${r.status},${r.checkIn||''},${r.checkOut||''}`)].join('\n');
    const blob=new Blob([csv],{type:'text/csv'});
    const a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download='attendance.csv';
    a.click();
  }
  return <PageTransition><div className="mb-6 flex items-center justify-between"><h1 className="gradient-text text-4xl font-black">Attendance</h1><button onClick={exportCsv} className="flex items-center gap-2 rounded-2xl border border-secondary/40 px-4 py-2 text-secondary"><Download className="h-4 w-4"/>Export CSV</button></div><div className="grid gap-6 xl:grid-cols-[1.2fr_.8fr]"><AttendanceCalendar records={data}/><div className="space-y-6"><CheckInButton/><WeeklyChart/></div></div><div className="mt-6"><DataTable rows={data as unknown as Record<string,unknown>[]} searchKey="employeeName" columns={[{key:'date',label:'Date'},{key:'employeeName',label:'Employee'},{key:'checkIn',label:'Check in'},{key:'checkOut',label:'Check out'},{key:'status',label:'Status',render:(r)=><StatusBadge status={String(r.status)}/>}]} /></div></PageTransition>;
}
