.class public final Ledu/singaporetech/travelapp/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "MainActivity.kt"


# annotations
.annotation runtime Lkotlin/Metadata;
    d1 = {
        "\u0000*\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0008\u0002\n\u0002\u0010\u000e\n\u0002\u0008\u0003\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\u0008\u0003\n\u0002\u0018\u0002\n\u0002\u0008\u0002\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u000e\u0010\u0007\u001a\u00020\u00082\u0006\u0010\t\u001a\u00020\nJ\u000e\u0010\u000b\u001a\u00020\u00082\u0006\u0010\t\u001a\u00020\nJ\u0012\u0010\u000c\u001a\u00020\u00082\u0008\u0010\r\u001a\u0004\u0018\u00010\u000eH\u0014J\u000e\u0010\u000f\u001a\u00020\u00082\u0006\u0010\t\u001a\u00020\nR\u0014\u0010\u0003\u001a\u00020\u0004X\u0086D\u00a2\u0006\u0008\n\u0000\u001a\u0004\u0008\u0005\u0010\u0006\u00a8\u0006\u0010"
    }
    d2 = {
        "Ledu/singaporetech/travelapp/MainActivity;",
        "Landroidx/appcompat/app/AppCompatActivity;",
        "()V",
        "TAG",
        "",
        "getTAG",
        "()Ljava/lang/String;",
        "currencyConverter",
        "",
        "view",
        "Landroid/view/View;",
        "emailFriend",
        "onCreate",
        "savedInstanceState",
        "Landroid/os/Bundle;",
        "temperatureConverter",
        "app_debug"
    }
    k = 0x1
    mv = {
        0x1,
        0x6,
        0x0
    }
    xi = 0x30
.end annotation


# instance fields
.field private final TAG:Ljava/lang/String;


# direct methods
.method public constructor <init>()V
    .locals 1

    .line 15
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    .line 17
    const-string v0, "MainActivity"

    iput-object v0, p0, Ledu/singaporetech/travelapp/MainActivity;->TAG:Ljava/lang/String;

    .line 15
    return-void
.end method


# virtual methods
.method public final currencyConverter(Landroid/view/View;)V
    .locals 3
    .param p1, "view"    # Landroid/view/View;

    const-string v0, "view"

    invoke-static {p1, v0}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    .line 28
    new-instance v0, Landroid/content/Intent;

    move-object v1, p0

    check-cast v1, Landroid/content/Context;

    const-class v2, Ledu/singaporetech/travelapp/CurrencyConverterActivity;

    invoke-direct {v0, v1, v2}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 29
    .local v0, "intent":Landroid/content/Intent;
    invoke-virtual {p0, v0}, Ledu/singaporetech/travelapp/MainActivity;->startActivity(Landroid/content/Intent;)V

    .line 30
    return-void
.end method

.method public final emailFriend(Landroid/view/View;)V
    .locals 3
    .param p1, "view"    # Landroid/view/View;

    const-string v0, "view"

    invoke-static {p1, v0}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    .line 38
    new-instance v0, Landroid/content/Intent;

    move-object v1, p0

    check-cast v1, Landroid/content/Context;

    const-class v2, Ledu/singaporetech/travelapp/EmailActivity;

    invoke-direct {v0, v1, v2}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 39
    .local v0, "intent":Landroid/content/Intent;
    invoke-virtual {p0, v0}, Ledu/singaporetech/travelapp/MainActivity;->startActivity(Landroid/content/Intent;)V

    .line 40
    return-void
.end method

.method public final getTAG()Ljava/lang/String;
    .locals 1

    .line 17
    iget-object v0, p0, Ledu/singaporetech/travelapp/MainActivity;->TAG:Ljava/lang/String;

    return-object v0
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 2
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .line 20
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 21
    const v0, 0x7f0b001e

    invoke-virtual {p0, v0}, Ledu/singaporetech/travelapp/MainActivity;->setContentView(I)V

    .line 24
    iget-object v0, p0, Ledu/singaporetech/travelapp/MainActivity;->TAG:Ljava/lang/String;

    const-string v1, "Hello, green robot"

    invoke-static {v0, v1}, Landroid/util/Log;->v(Ljava/lang/String;Ljava/lang/String;)I

    .line 25
    return-void
.end method

.method public final temperatureConverter(Landroid/view/View;)V
    .locals 3
    .param p1, "view"    # Landroid/view/View;

    const-string v0, "view"

    invoke-static {p1, v0}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    .line 33
    new-instance v0, Landroid/content/Intent;

    move-object v1, p0

    check-cast v1, Landroid/content/Context;

    const-class v2, Ledu/singaporetech/travelapp/TempConverterActivity;

    invoke-direct {v0, v1, v2}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 34
    .local v0, "intent":Landroid/content/Intent;
    invoke-virtual {p0, v0}, Ledu/singaporetech/travelapp/MainActivity;->startActivity(Landroid/content/Intent;)V

    .line 35
    return-void
.end method
