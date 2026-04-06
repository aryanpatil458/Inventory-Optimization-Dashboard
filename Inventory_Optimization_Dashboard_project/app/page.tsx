import { Download } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function Home() {
  return (
    <main className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Inventory Dataset</CardTitle>
          <CardDescription>
            Retail inventory data with 100 transactions across 20 products
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <div className="text-sm text-muted-foreground space-y-1">
            <p><strong>Records:</strong> 100 transactions</p>
            <p><strong>Products:</strong> 20 items</p>
            <p><strong>Categories:</strong> Tools, Electrical, Paint, Garden</p>
            <p><strong>Date Range:</strong> Jan - Apr 2024</p>
          </div>
          <Button asChild className="w-full">
            <a href="/retail_inventory_data.csv" download="retail_inventory_data.csv">
              <Download className="mr-2 h-4 w-4" />
              Download CSV
            </a>
          </Button>
        </CardContent>
      </Card>
    </main>
  )
}
